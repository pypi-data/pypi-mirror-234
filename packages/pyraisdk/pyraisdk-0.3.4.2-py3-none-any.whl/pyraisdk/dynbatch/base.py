from abc import ABC, abstractmethod
from typing import Any, List

class BaseModel(ABC):
    '''Base class for models to inherit from
    '''
    
    @abstractmethod
    def predict(self, items: List[Any]) -> List[Any]:
        '''Model predict function
        
        Abstract method which need to be implemented in subclass. It receives
        a bunch of input items, and output same number of predict results.
        
        Args:
            items: Input data items
            
        Returns:
            Predict results for each input data item
        '''
        pass
        
        
    def preprocess(self, items: List[Any]) -> List[Any]:
        '''Preprocessing steps to convert raw data into the form required by your model
        
        Put your precessing logic into this function so that metrics like counting
        and duration will be handled correctly. For example, perform any JSON transformations
        you need here

        Default implementation is enough if you just want to put every thing in the 'predict' function.
        
        Args:
            items: Input data items
            
        Returns:
            Preprocessing results for each input data item
        '''
        return items
    
