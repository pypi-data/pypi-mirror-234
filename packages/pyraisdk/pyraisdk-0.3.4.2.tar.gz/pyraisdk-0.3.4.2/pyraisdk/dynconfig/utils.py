
import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List


class Call:
    def __init__(self, *args: Any, **kwargs: Any):
        self.args = args
        self.kwargs = kwargs


@dataclass
class _BatchItem:
    call: Call
    result: Any


async def run_async_batch(
    func: Callable[..., Awaitable[Any]],
    calls: List[Call],
    max_retry_num: int = 2,
    max_iter_fail_ratio: float = 0.5,
) -> List[Any]:
    ''' Execute async operations concurrently.
        Args:
            func: async funcion
            calls: batch args, each element gives the parameter of an operation.
            max_retry_num: max retry number.
            max_iter_fail_ratio: Allowed max failure ratio in each retry.
            
        Returns:
            Results for each batch item.
    '''
    ex = Exception('unexpected error')
    call_batch = [_BatchItem(call=c, result=None) for c in calls]
    batch = call_batch[:]
    for _ in range(max_retry_num + 1):
        results = await asyncio.gather(
            *[func(*item.call.args, **item.call.kwargs) for item in batch],
            return_exceptions=True,
        )
        assert len(batch) == len(results)
        batch_retry = []
        for item, result in zip(batch, results):
            if isinstance(result, Exception):
                batch_retry.append(item)
                ex = result
            else:
                item.result = result

        if batch_retry:
            if len(batch_retry) > len(batch) * max_iter_fail_ratio:
                raise Exception(f'too high failure ratio for async batch: {len(batch_retry)} / {len(batch)}') from ex
            else:
                batch = batch_retry
        else:
            return [item.result for item in call_batch]
    
    # `ex` is just a sample error. 
    # Multiple errors may occur in a batch, and most of them should be similar.
    # Putting one of them into the raised exception should be enough.
    raise Exception('too many retries for async batch') from ex
