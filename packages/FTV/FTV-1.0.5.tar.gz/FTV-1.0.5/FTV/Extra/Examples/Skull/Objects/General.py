

# TODO architecture construct this class
class Data:
    def __init__(self, *args):
        """ Hold and process dataframes.

        DataFrames can be passed to StaticData object on creation:
            d = StaticData(pandas.Dataframe(...))
        DataFrames can be added at certain position into existing StaticData object:
            d = StaticData()
            d.put(pandas.Dataframe(...), 0)
        StaticData to show can be filtered with .select() with needed column names and/or DataFrame index:
            d.select(columns=['a_x', 'm_h'])
            d.select(index=1)
            d.select(columns=['a_x', 'm_h'], index=0)
        Filtered/selected Dats can be seen with .show:
            d.show()
        Merged data for charting can be retrieved with .chartify()
            d.chartify()

        :param args: one or more DataFrame, optional
        """
        self.data_raw = [pandas.DataFrame() for i in range(MAX_FILES_TO_LOAD)]
        if args:
            cnt = 0
            for i, df in enumerate(args):
                self.put(df, i)

        self.data_show = self.data_raw[:]
        self._autoscale = False
        self._columns_to_show = []
        self._files_to_show = {i: True for i in range(MAX_FILES_TO_LOAD)}
        self.auto_scale()
        self.legend = []

    def put(self, df: pandas.DataFrame, index):
        self.data_raw[index] = df
        self._files_to_show[index] = True
        # Delete useless columns
        useless_cols = list(col for col in self.columns if 'running' in col.lower())
        useless_cols.append('ts')
        try:
            self.data_raw[index].drop(columns=useless_cols, inplace=True)
        except KeyError:
            pass

        try:
            # Keep filter if initialized
            if self._columns_to_show:
                self.select(self._columns_to_show)
            else:
                self.select()
        except KeyError:
            sg.popup_error('', 'Loaded file has old header format.', 'Use script from readme.md to fix the input file.',
                           '',
                           title='Skensor: StaticData error', font='Any 15', keep_on_top=True, line_width=200)
            sys.exit()

        self.auto_scale()

    def clear(self, index):
        """ Clear certain index from StaticData to show"""
        self._files_to_show[index] = False
        self.data_show[index] = pandas.DataFrame()

    @property
    def columns(self) -> list:
        return list(self.data_raw[0].columns)

    @property
    def columns_to_show(self) -> list:
        return list(self.data_show[0].columns)

    def _set_data_by_index(self, index):
        if not self._columns_to_show:
            # Clear data to show at certain index if the entire file masked out.
            self.clear(index)
        elif not self.data_raw[index].empty:
            self.data_show[index] = self.data_raw[index][self._columns_to_show]

    def select(self, columns: list = None, index=None):
        """ Copy from self.data_raw to self.data_show only specified `columns`"""
        self._columns_to_show = columns if columns else self.columns

        # Quick copy of selected columns only into DataFrame to present.
        if index is None:
            for i in range(MAX_FILES_TO_LOAD):
                if self._files_to_show[i]:
                    self._set_data_by_index(i)
        else:
            self._files_to_show[index] = True
            self._set_data_by_index(index)

    @property
    def autoscale(self):
        return self._autoscale

    @autoscale.setter
    def autoscale(self, value: bool):
        # Use auto-scale as property because it is not always called with known value and should use internal attribute.
        self._autoscale = value
        self.auto_scale()

    def auto_scale(self):
        """ make all dataframes to show with equal scale """

        print('>> auto_scale called, enable:', self._autoscale)
        if self._autoscale:
            try:
                scaler = MinMaxScaler()
                for i in range(MAX_FILES_TO_LOAD):
                    df_np = scaler.fit_transform(self.data_show[i].to_numpy())
                    self.data_show[i] = pandas.DataFrame(df_np, columns=self._columns_to_show)
            except ValueError:
                print('No data yet...', self.data_show[0].columns)

        else:
            self.select(self._columns_to_show)

    def show(self, lines: int = 3, index=None) -> str:
        """ Returns string of data samples.
        :param lines - How many lines to present from each dataframe, defaults to 3
        :param index - Which dataframe to expose, defaults to all.
        """

        res = ''

        if index is None:
            for d in self.data_show:
                res += str(d[:lines]) + '\n'
        else:
            res = str(self.data_show[index][:lines])

        return res

    def chartify(self, ewm_span=1):
        """ Transform data to show into unified DataFrame with prefixes of original DataFrame index.

        :returns df - merged DataFrame
        :returns legend - list
        """

        self.auto_scale()
        # Merge all raw dataframe into one DF for charting. Rename columns with prefixes of the original Dataframe ID.
        filtered_dataframes = []
        orig_cols = self.columns_to_show
        for idx, current_df in enumerate(self.data_show):
            # Smooth the numbers to filter out the noise
            current_df = current_df.ewm(span=ewm_span).mean()
            new_cols = list(f'D{idx + 1}_{col}' for col in orig_cols)
            rename_dict = dict(zip(orig_cols, new_cols))
            filtered_dataframes.append(current_df.rename(columns=rename_dict))

        res = pandas.concat(filtered_dataframes, axis=1)

        self.legend = res.columns
        return res, self.legend

