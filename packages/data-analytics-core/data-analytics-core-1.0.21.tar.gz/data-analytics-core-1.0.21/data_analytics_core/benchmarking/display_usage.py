from typing import Union
import psutil
# custom imports
from data_analytics_core.logger import da_logger
from data_analytics_core.benchmarking.worker_class import MetricsWorker


# TODO: Reduce complexity of the outer decorator, include moar modules
def display_usage_metrics(
	delay_metrics_check_in_secs: Union[float, int] = 0.5,
	printed_bars: int = 25,
	output_logs: bool = True,
	output_mean_metrics: bool = False,
	is_method_from_a_class=False,
	*args,
	**kwargs
):

	# TODO: check if decorated function have a return what happens with the output

	def display_metrics_wrapper(function_to_eval):
		if is_method_from_a_class:
			def metrics_for_method(self):
				worker = MetricsWorker(
					function_to_run=print_metrics,
					delay_in_secs=delay_metrics_check_in_secs,
					output_mean_metrics=output_mean_metrics)
				worker.start()
				function_to_eval(self, *args, **kwargs)
				worker.stop_thread()
			return metrics_for_method
		else:
			def metrics_for_function():
				worker = MetricsWorker(
					function_to_run=print_metrics,
					delay_in_secs=delay_metrics_check_in_secs,
					output_mean_metrics=output_mean_metrics)
				worker.start()
				function_to_eval(*args, **kwargs)
				worker.stop_thread()
			return metrics_for_function

	def print_metrics(
		bars: int = printed_bars, output_print_logs: bool = output_logs,
		mean_metrics_output: bool = output_mean_metrics
	) -> Union[dict, None]:
		# env_vars
		cpu_usage = psutil.cpu_percent(percpu=True)
		mem_usage = psutil.virtual_memory().percent
		list_of_metrics = {}
		# cpu calculation
		if isinstance(cpu_usage, list):
			cpu_number = 0
			for cpu in cpu_usage:
				cpu_number = cpu_number + 1
				cpu_percent = (cpu/100)
				if output_print_logs:
					cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
					da_logger.info(f'\nCPU_{cpu_number} Usage: |{cpu_bar}| {cpu:.3f}% ')
				if mean_metrics_output:
					list_of_metrics.update({f'CPU_{cpu_number}': cpu_percent})

		else:
			cpu_percent = (cpu_usage / 100)
			if output_print_logs:
				cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
				da_logger.info(f'\nCPU Usage: |{cpu_bar}| {cpu_usage:.3f}% ')
			if mean_metrics_output:
				list_of_metrics.update({'CPU': cpu_percent})
		# memory calculation
		mem_percent = (mem_usage/100)
		if output_print_logs:
			mem_bar = '█' * int(mem_percent * bars) + '-' * (bars - int(mem_percent * bars))
			da_logger.info(f'\nMEM Usage: |{mem_bar}| {mem_usage:.3f}% ')
		if mean_metrics_output:
			list_of_metrics.update({'MEM': mem_percent})
		return list_of_metrics

	return display_metrics_wrapper
