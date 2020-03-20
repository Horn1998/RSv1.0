from Common.LogProcess.Logger import Logger
class EngineFactory:
    def __init__(self, opts):
        self.opts = opts



    #工厂模式
    def build(self):
        try:
            if self.opts['engine'] == 'TPEngine':
                pass
            elif self.opts['engine'] == 'RSEngine':
                if 'option' in self.opts.keys() and self.opts['option']:
                    module_meta = __import__('Recommand', globals(), locals(), [self.opts['option']], level=1)
                    class_meta = getattr(module_meta, self.opts['option'])
                    obj = class_meta(self.opts)
                    obj.run()

        except Exception as ex:
            Logger('error').get_log().error(ex)



    def run(self):
        print('engine is running')
        pass