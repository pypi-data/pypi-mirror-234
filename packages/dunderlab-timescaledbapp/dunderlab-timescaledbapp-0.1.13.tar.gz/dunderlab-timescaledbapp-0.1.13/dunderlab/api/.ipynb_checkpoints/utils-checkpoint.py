import json
import cProfile
import pstats
import io
import numpy as np


# ----------------------------------------------------------------------
def JSON(obj, max_list_len=5, indent=2):
    def truncate_list(lst):
        if len(lst) > max_list_len:
            return lst[:max_list_len] + ['...']
        else:
            return lst

    # ----------------------------------------------------------------------
    def format_list(lst):
        if len(lst) > max_list_len:
            return '[' + ', '.join(str(item) for item in lst[:max_list_len]) + ', ...]'
        else:
            return '[' + ', '.join(str(item) for item in lst) + ']'

    # ----------------------------------------------------------------------
    def truncate_and_format_lists(obj, level=0):
        if isinstance(obj, list):
            return format_list(truncate_list([truncate_and_format_lists(item, level + 1) for item in obj]))
        elif isinstance(obj, dict):
            result = '\n' + ' ' * (indent * (level)) + '{\n'
            for key, value in obj.items():
                result += ' ' * (indent * (level + 1)) + f'"{key}": {truncate_and_format_lists(value, level+1)},\n'
            result += ' ' * (indent * level) + '}'
            return result
        else:
            return json.dumps(obj, indent=indent)

    truncated_obj = truncate_and_format_lists(obj)
    formatted_obj_str = json.loads(json.dumps(truncated_obj, indent=indent))
    formatted_obj_str = formatted_obj_str.replace(', [...]', ', ...]')
    formatted_obj_str = formatted_obj_str.replace('[...', '[ ...')
    formatted_obj_str = formatted_obj_str.replace(']...', ', ...]')
    print(formatted_obj_str)


########################################################################
class Profile:

    # ----------------------------------------------------------------------
    def __init__(self, sort_key=pstats.SortKey.CUMULATIVE, stats=('ncalls', 'primitive calls', 'time')):
        self.sort_key = sort_key
        self.stats = stats

    # ----------------------------------------------------------------------
    def __enter__(self):
        self.pr = cProfile.Profile()
        self.pr.enable()

    # ----------------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats(self.sort_key)
        ps.print_stats(*self.stats)
        print(s.getvalue())
        self.execution_output = s.getvalue()
        total_time = sum(st[2] for st in ps.stats.values())
        self.execution_time = total_time

    # ----------------------------------------------------------------------
    def __str__(self):
        return self.execution_output


profile = Profile()


# def get_data(trials_response):
    # """"""
    # data = []
    # classes = []

    # if isinstance(trials_response, dict):
        # trials_response = [trials_response]

    # for trials_set in trials_response:
        # if trials_set.get('detail', None) == 'Invalid page.':
            # continue
        # t_ = []
        # for trials in trials_set['results']:
            # t = []
            # if isinstance(trials, list):
                # for trial in trials:
                    # t.append(trial['values'])
                # classes.append(trial['trial_class'])
            # elif isinstance(trials, dict):
                # t_.append(trials['values'])

            # if t:
                # data.append(t)
        # if t_:
            # data.append(t_)

    # classes = np.array(classes)

    # if classes.size:
        # return np.array(data), classes
    # else:
        # return np.concatenate(data, axis=1)

# def get_data(data_trials_response):

    # if isinstance(data_trials_response, dict):
        # data_trials_response = [data_trials_response]

    # data = []
    # classes = []

    # for data_trials in data_trials_response:
        # if data_trials.get('detail', None) == 'Invalid page.':
            # continue

        # for trial in data_trials['results']:
            # t = []
            # for channel in trial['values']:
                # t.append(trial['values'][channel])
            # data.append(t)
            # classes.append(trial['trial_class'])

    # data = np.array(data)
    # classes = np.array(classes)

    # del data_trials_response
    # return data, classes

def get_data(data_trials_response):

    if isinstance(data_trials_response, dict):
        data_trials_response = [data_trials_response]

    data = []
    classes = []

    for data_trials in data_trials_response:
        if data_trials.get('detail', None) == 'Invalid page.':
            continue

        if isinstance(data_trials['results'], dict):

            t = []
            for channel in data_trials['results']['values']:
                t.append(data_trials['results']['values'][channel])
            data.append(t)

        else:
            for trial in data_trials['results']:
                t = []

                for channel in trial['values']:
                    t.append(trial['values'][channel])
                data.append(t)
                classes.append(trial['trial_class'])

    data = np.array(data)
    classes = np.array(classes)

    del data_trials_response

    if classes.size:
        return data, classes
    else:
        return np.concatenate(data, axis=0)
