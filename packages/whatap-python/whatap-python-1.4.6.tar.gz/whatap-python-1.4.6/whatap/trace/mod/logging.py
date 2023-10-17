import sys
from whatap import DateUtil, conf
from whatap.net.udp_session import UdpSession
from whatap.pack import logSinkPack
from whatap.trace.trace_context_manager import TraceContextManager
import whatap.io as whatapio

loguru_injection_processed = False
def instrument_loguru(module):
    global loguru_injection_processed
    def wrapper(fn):
        def trace(*args, **kwargs):
            if not conf.trace_loguru_enabled:
                return fn(*args, **kwargs)

            if len(args) <=1:
                return fn(*args, **kwargs)

            ctx = TraceContextManager.getLocalContext()
            if not ctx:
                return fn(*args, **kwargs)

            category = "AppLog"
            tags = {'@txid': str(ctx.id)} if ctx is not None else {}

            filename = None
            record = args[1]
            levelname = record["level"].name
            msg = record["message"]
            fields = {"filename": filename}

            content = f"{levelname}  {msg}"

            p = logSinkPack.getLogSinkPack(
                t=DateUtil.now(),
                category=f"{category}",
                tags=tags,
                fields=fields,
                line=DateUtil.now(),
                content=content
            )

            p.pcode = conf.PCODE
            bout = whatapio.DataOutputX()
            bout.writePack(p, None)
            packbytes = bout.toByteArray()

            UdpSession.send_relaypack(packbytes)
            return fn(*args, **kwargs)
        return trace
    if not loguru_injection_processed:
        module.Handler.emit = wrapper(module.Handler.emit)
        loguru_injection_processed = True

logging_injection_processed = False
def instrument_logging(module):
    global logging_injection_processed
    def wrapper(fn):
        def trace(*args, **kwargs):
            if not conf.trace_logging_enabled:
                return fn(*args, **kwargs)

            ctx = TraceContextManager.getLocalContext()
            record = args[1]

            ##1.3.6 Backward Compatibility
            setattr(record, "txid", None)

            if not ctx:

                return fn(*args, **kwargs)

            instance = args[0]
            category = "AppLog"

            # logger_name = getattr(instance, "name", None)
            # if logger_name and logger_name == "whatap":
            #     category = "#AppLog"

            filehandler = [handler for handler in instance.handlers if handler.__class__.__name__ == "FileHandler"]
            filename = None
            if filehandler and len(filehandler)>0:
                filehandler = filehandler[0]
                if hasattr(filehandler, "baseFilename"):
                    filename = filehandler.baseFilename

            levelname = getattr(record, "levelname", None)
            msg = record.getMessage()

            fields = {"filename": filename}

            content = f"{levelname}  {msg}"

            tags = {'@txid': ctx.id} if ctx is not None else {}

            p = logSinkPack.getLogSinkPack(
                t=DateUtil.now(),
                category=f"{category}",
                tags=tags,
                fields=fields,
                line=DateUtil.now(),
                content=content
            )

            p.pcode = conf.PCODE
            bout = whatapio.DataOutputX()
            bout.writePack(p, None)
            packbytes = bout.toByteArray()

            UdpSession.send_relaypack(packbytes)
            return fn(*args, **kwargs)
        return trace

    if not logging_injection_processed:
        module = sys.modules.get("logging")
        module.Logger.callHandlers = wrapper(module.Logger.callHandlers)
        logging_injection_processed = True