import json
import numpy as np
from vininfo import Vin
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests import Session
from .config import STANDARD_VAR_NAMES_NHTSA


class ExternalApiSession(Session):
    """
    Custom session for external APIs.

    Inherits from the `requests.Session` class and sets additional headers.
    """
    def __init__(self, *args, **kwargs):
        super(ExternalApiSession, self).__init__(*args, **kwargs)
        self.headers.update({"Accept-Charset": "utf-8"})

class ExternalApiVin:
    """
    Base class for external VIN decoding services.

    Provides methods for looking up VIN information and processing responses.
    """
    def __init__(self): pass
    def lookup_vin(self, vin, **kwargs): 
        """
        Lookup VIN information.

        Args:
            vin (str or list): The VIN(s) to lookup.
            **kwargs: Additional keyword arguments.

        Returns:
            dict or list: The decoded VIN information.

        Raises:
            ValueError: If vin is None.
        """
        pass
    def process_response(self, response): 
        """
        Process the response from the external service.

        Args:
            response: The response from the external service.

        Returns:
            dict: Processed VIN information.
        """
        pass
        
    
class VinNHTSA(ExternalApiVin):
    """
    VIN decoding using the NHTSA (National Highway Traffic Safety Administration) API.

    Provides methods for decoding VINs using the NHTSA API.
    """
    def __init__(self,host="https://vpic.nhtsa.dot.gov/api/vehicles/"):
        super().__init__()
        if host: self.host=host
        self.session = ExternalApiSession()
        self.session.mount(self.url, HTTPAdapter(pool_connections=2, max_retries=5))
            
    @property
    def url(self):
        return self.host
    
    def lookup_vin(self, vin, **kwargs):
        if vin is None: raise ValueError("Vin is required")
        if isinstance(vin, str): response=self.decode_vin(vin, kwargs.get("model_year", None))
        elif isinstance(vin, list): response=self.decode_vin_batch(vin)
        else: return {'wmi':None, 'vds':None, 'vis':None}
        return self.process_response(response)
    
    def standardize(self, data):
        if isinstance(data, dict): 
            return {STANDARD_VAR_NAMES_NHTSA.get(key, key): self.standardize(value) for key, value in data.items()}
        elif isinstance(data, list): return [self.standardize(item) for item in data]
        else: return data
        
    def process_response(self, response):
        
        if (not response) or (response.status_code >= 400): return {}
        
        response = response.json()["Results"]
        if isinstance(response, dict): response=[response]
        details,rdetails=['AxleConfiguration', 'Axles', 'BatteryInfo', 'BodyCabType', 'BrakeSystemType',
                         'CoolingType', 'DriveType', 'EngineConfiguration', 'EngineCylinders', 'EngineManufacturer',
                         'EngineModel', 'FuelInjectionType', 'FuelTypeSecondary', 'Manufacturer', 'OtherEngineInfo', 
                          'Seats', 'Series2', 'TPMS', 'Trim2', 'VehicleType', 'WheelBaseType', 'Wheels'],{}
        results=[]
        for item in response:
            item_stdr = self.standardize(item)
            rdetails={k:item_stdr[k] for k in details if (item_stdr.get(k,None) and ('Not Applicable' not in str(item_stdr.get(k,''))))}
            res={k:v for k,v in {
                "source": 'https://vpic.nhtsa.dot.gov/',
                "maker": item_stdr.get('Make', None),
                "model": item_stdr.get('Model', None),
                "serie": item_stdr.get('Series', None),
                "trim": item_stdr.get('Trim', None),
                "country": item_stdr.get('PlantCountry', None),
                "year": int(item_stdr.get('ModelYear', None)) if item_stdr.get('ModelYear', None) else None,
                "fuel_type": item_stdr.get('FuelTypePrimary', None),
                "transmission_type": item_stdr.get('TransmissionStyle', None),
                "body_type": item_stdr.get('BodyClass', None),
                "other": rdetails if rdetails else None
            }.items() if v}
            if len(res)>2: results.append(res)
        if len(results)==0: return {'wmi':None, 'vds':None, 'vis':None}
        return results[0] if len(results)==1 else results

    def decode_vin(self, vin, model_year=None):
        endpoint = "DecodeVinValues"
        
        if not len(vin) in range(6, 17 + 1): 
            raise ValueError("Vin must be at least 6 characters and at most 17 characters")
        if model_year and model_year < 1981:
            raise ValueError("Model year must be 1981 or later")

        params = {"modelyear": model_year} if model_year else {}
        params["format"] = "json"

        api = urljoin(self.url, f"{endpoint}/{vin}")
        response = self.session.get(api, params=params)

        return response

    def decode_vin_batch(self, vins):
        endpoint = "DecodeVINValuesBatch"
        
        if not len(vins) in range(1, 50 + 1):
            raise ValueError("Pass at least one VIN, and at most 50 VINs")
              
        data={"data": ";".join(vins), "format": "json"}

        api = urljoin(self.url, endpoint)
        response = self.session.post(url=api, data=data)

        return response


class VinInfo(ExternalApiVin):
    """
    VIN decoding using the vininfo Python library.

    Provides methods for decoding VINs using the vininfo library.
    """
    def __init__(self):
        super().__init__()
    
    def lookup_vin(self, vin, **kwargs):
        if vin is None: 
            raise ValueError("Vin is required")
        if isinstance(vin, str): 
            return self.process_response(Vin(vin))
        elif isinstance(vin, list):
            result=[]
            for v in vin:
                result.append(self.process_response(Vin(v)))
            return result
        return {'wmi':None, 'vds':None, 'vis':None}
    
    def process_response(self, response):
        if not response: return {}
        details,rdetails=['body', 'engine', 'plant', 'transmission'],{}
        if response.details: rdetails={k:getattr(response.details, k).name for k in details}
        try: years=int(response.years[0]) if isinstance(response.years, list) else response.years
        except: years=None
        return {"source": "vininfo_python",
                 "wmi": response.wmi,
                 "model": response.details.model.name if rdetails else None,
                 "serie": response.details.serial.name if rdetails else None,
                 "vds": response.vds,
                 "vis": response.vis,
                 "maker": response.manufacturer,
                 "country": response.country,
                 "year": years,
                 "other": {k:v for k,v in {"region": response.region, **rdetails}.items() if v is not None}}
