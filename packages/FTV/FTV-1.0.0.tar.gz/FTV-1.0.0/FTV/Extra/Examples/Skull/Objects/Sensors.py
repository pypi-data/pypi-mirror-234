import re
from abc import ABC, ABCMeta


# TODO architecture construct this interface
class SensorInterface(ABCMeta):
    pass


# TODO architecture refactor this class
class Sensor(SensorInterface):
    def __init__(self, mac, id):
        """
        :param mac: string hexadecimal bytes separated with comma.
        :param id: string 'l' or 'r' or 'b'
        """
        self.mac = mac
        self.power = 0
        self.rec = 0
        self.mv = 0
        self.id = id

    def update(self, power, rec, mv) -> bool:
        """ Updates internal attributes with provided values.

            :returns:
                True if values updated (were changed)
                False if older values kept the same.
        """
        res = self.power == power and self.rec == rec and self.mv == mv
        self.power = power
        self.rec = rec
        self.mv = mv
        return not res

    def present(self):
        return self.power and self.mv

    @property
    def verbose_id(self):
        return 'Right' if 'r' == self.id else 'Left' if 'l' == self.id else 'Back' if 'b' == self.id else 'Error'

    def save_data(self, data, window):
        """
        Extract data from mixed sensors reading. Saves the data as csv file.

        :param data:  raw format
        :param window:
        :return:
            path of the stored data.
            error string if error happened.
        """

        def get_radio_button_value(args):  # giving unknown number of parameters
            for v in args:
                value = window[v].get()
                if value:
                    return re.findall('-.*-([a-z]+)-', v)[0]

        error = ''
        my_list = re.findall('(?i).*%s.*\s([\d,-]{50,})' % self.mac, data)
        # Drop all dups from the list if any
        my_data = list([v for i, v in enumerate(my_list[:-2]) if v != my_list[i + 1]])
        try:
            start = int(my_list[0].split(',')[0]) / 1000
            end = int(my_list[-1].split(',')[0]) / 1000
        except IndexError:
            start = 0
            end = 0
        print('>> ', self.id, 'run duration:', end - start, 'seconds')
        l_csv = '\n'.join(my_data)
        if not l_csv:
            error = f'{self.verbose_id} sensor data missing.\n'

        asserted_weight = [k for k in window.key_dict.keys() if 'wgt' in k and window[k].get()][0]
        weight = re.findall('wgt-(\w+)-', asserted_weight)[0]
        gender = 'm' if window['-gdr-m-'].get() else 'f'
        outlier_suspect = 'yes' if window['-outlier-'].get() else 'no'
        medicated = 'yes' if window['-medicated-'].get() else 'no'
        short_leg = get_radio_button_value([i[0] for i in short_leg_group])
        gait_failure = get_radio_button_value([i[0] for i in gait_failure_group])
        dominant_side = get_radio_button_value([i[0] for i in dominant_side_group])
        path = 'data/' + window['-p_code-'].get() + '/' + datetime.now().strftime('%d_%m_%Y_%H_%M') + '/'

        value_list = [''.join(re.findall('\w', window['-subluxation-'].get())),
                      window['-location-'].get(),
                      self.id, window['-age-'].get(),
                      weight,
                      gender,
                      measure_type.replace('-', ''),
                      window['-duration-'].get(),
                      window['-pain_loc-'].get(),
                      window['-radiating-'].get(),
                      window['-pain_lvl-'].get(),
                      window['-rate-'].get(),
                      short_leg,
                      window['-ple_l-'].get(),
                      window['-ple_r-'].get(),
                      gait_failure,
                      window['-p_pressure_l-'].get(),
                      window['-p_pressure_r-'].get(),
                      window['-severity-'].get(),
                      outlier_suspect,
                      medicated,
                      dominant_side]

        f_name = '_'.join(value_list) + '.csv'
        header = "ts,running_min.x,running_min.y,running_min.z,running_max.x,running_max.y,running_max.z,a_x,a_y,a_z,m_x,m_y,m_z,m_h,g_x,g_y,g_z\n"
        save(path + f_name, header + l_csv)
        return path, error


# TODO architecture construct this class
class VirtualSensor(SensorInterface):
    pass
