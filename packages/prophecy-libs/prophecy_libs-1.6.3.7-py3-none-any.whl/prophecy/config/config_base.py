# WARNING - Do not add import * in this module


class ConfigBase:
    def updateSpark(self, spark):
        self.spark = spark

    def get_dbutils(self, spark):
        try:
            dbutils  # Databricks provides an instance of dbutils be default. Checking for it's existence
            return dbutils
        except NameError:
            try:
                from pyspark.dbutils import DBUtils

                _dbutils = DBUtils(spark)
            except:
                try:
                    import IPython

                    _dbutils = IPython.get_ipython().user_ns["dbutils"]
                except Exception as e:
                    from prophecy.test.utils import ProphecyDBUtil

                    _dbutils = ProphecyDBUtil

            return _dbutils

    def get_int_value(self, value):
        if value is not None:
            return int(value)
        else:
            return value

    def get_float_value(self, value):
        if value is not None:
            return float(value)
        else:
            return value

    def get_bool_value(self, value):
        if value is not None:
            return bool(value)
        else:
            return value

    # Old function, keeping it for backward compatibility
    def generate_object(self, value, cls):
        if isinstance(value, list):
            return [self.generate_object(x, cls) for x in value]
        elif isinstance(value, dict):
            return cls(**value)
        return value

    # Old function, keeping it for backward compatibility
    def get_object(self, default, override, cls):
        if override == None:
            return default
        else:
            return self.generate_object(override, cls)

    def generate_config_object(self, spark, value, cls):
        if isinstance(value, list):
            return [self.generate_config_object(spark, x, cls) for x in value]
        elif isinstance(value, dict):
            return cls(**{**{"prophecy_spark": spark}, **value})
        return value

    def get_config_object(self, spark, default, override, cls):
        if override == None:
            return default
        else:
            return self.generate_config_object(spark, override, cls)
