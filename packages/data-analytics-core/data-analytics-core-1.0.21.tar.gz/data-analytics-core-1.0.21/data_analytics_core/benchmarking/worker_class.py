import time
from threading import Thread, Event
import pandas as pd

from data_analytics_core.logger import da_logger


class MetricsWorker(Thread):
    def __init__(self, function_to_run, event: Event = Event(),
                 delay_in_secs: float = 0.5,
                 output_mean_metrics: bool = False,
                 *args, **kwargs):
        # set the thread's event manager
        self.event = event
        super().__init__(args=(self.event,), *args, **kwargs)
        # other vars
        self.delay_in_secs = delay_in_secs
        self.function_to_run = function_to_run
        self.args = args
        self.kwargs = kwargs
        self.output_mean_metrics = output_mean_metrics

    def run(self):
        """Method representing the thread's activity.
        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.
        """
        if self.output_mean_metrics is False:
            while self.event.is_set() is False:
                self.function_to_run(*self.args, **self.kwargs)
                time.sleep(self.delay_in_secs)
            self.event.clear()
        else:
            list_of_dicts_of_metrics = []
            while self.event.is_set() is False:
                list_of_dicts_of_metrics.append(self.function_to_run(*self.args, **self.kwargs))
                time.sleep(self.delay_in_secs)
            self.event.clear()
            metrics_df = pd.DataFrame(list_of_dicts_of_metrics)
            da_logger.info(f'Min, mean, max and stdev values (in parts per unit) for metrics during evals:'
                            f'{da_logger.new_line()}'
                            f'Min: {dict(metrics_df.min().round(3))} ,{da_logger.new_line()}'
                            f'Mean: {dict(metrics_df.mean().round(3))} ,{da_logger.new_line()}'
                            f'Max: {dict(metrics_df.max().round(3))} ,{da_logger.new_line()}'
                            f'Stdev: {dict(metrics_df.std().round(3))}')

    def stop_thread(self):
        self.event.set()

