import grpc
import Oasys.gRPC

class Connection():

    def __init__(self, program, port, memory, hostname, debug=False):
        self.debug = debug

        self.dbg("Connecting to {} at {}:{}".format(program, hostname, port))

        self.program  = program
        self.hostname = hostname
        self.channel  = grpc.insecure_channel('{}:{}'.format(hostname, port))
        self.stub     = Oasys.gRPC.oasys_pb2_grpc.InterfaceStub(self.channel)

# Initialise
        request = Oasys.gRPC.oasys_pb2.Memory()
        request.size = memory
        self.dbg("Calling Initialise")
        response = self.stub.Initialise(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))


    def constructor(self, objtype, *args):
# Constructor
        request = Oasys.gRPC.oasys_pb2.ConstructorRequest()
        request.type = objtype


        self.dbg("Calling {} Constructor with {} args".format(request.type, len(args)))

        for arg in args:
# If we get to a default arg then no more args to pass
            if arg is Oasys.gRPC.defaultArg:
                break

# If the arg is a tuple then it must be the last arg (for varargs).
# If the length of the tuple is 0 then don't send it
            elif isinstance(arg, tuple) and len(arg) == 0:
                break

            self.add_request_arg(request, arg)


        response = self.stub.Constructor(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK
        assert response.value.HasField("itemarg")
        self.dbg("Value {} handle {}".format(response.value.itemarg.t, response.value.itemarg.h))

        return response.value.itemarg.h


    def destructor(self, objtype, handle):
# Destructor
        request = Oasys.gRPC.oasys_pb2.DestructorRequest()

        request.item.t = objtype
        request.item.h = handle

        self.dbg("Calling {} Destructor with handle {}".format(objtype, handle))

        response = self.stub.Destructor(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK


    def functionCall(self, func, *args):
# Function call
        request = Oasys.gRPC.oasys_pb2.FunctionRequest()
        request.func = func


        self.dbg("Calling Function {} with {} args".format(func, len(args)))

        for arg in args:
# If we get to a default arg then no more args to pass
            if arg is Oasys.gRPC.defaultArg:
                break

# If the arg is a tuple then it must be the last arg (for varargs).
# If the length of the tuple is 0 then don't send it
            elif isinstance(arg, tuple) and len(arg) == 0:
                break

            self.add_request_arg(request, arg)


        response = self.stub.Function(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK

# Decode the response value
        return self.decode_response_value(response.value)


    def instanceGetter(self, objtype, handle, name):
# Getter
        request = Oasys.gRPC.oasys_pb2.InstanceGetRequest()

        request.item.t   = objtype
        request.item.h   = handle
        request.property = name

        self.dbg("Calling {} Getter with handle {} property {}".format(objtype, handle, name))

        response = self.stub.InstanceGet(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK

# Decode the response value
        return self.decode_response_value(response.value)


    def instanceSetter(self, objtype, handle, name, value):
# Setter
        request = Oasys.gRPC.oasys_pb2.InstanceSetRequest()

        request.item.t   = objtype
        request.item.h   = handle
        request.property = name

        self.encode_request_value(request, value)

        self.dbg("Calling {} Setter with handle {} property {}={}".format(objtype, handle, name, value))

        response = self.stub.InstanceSet(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK


    def instanceMethod(self, objtype, handle, method, *args):
# Instance Method call
        request = Oasys.gRPC.oasys_pb2.InstanceMethodRequest()

        request.item.t = objtype
        request.item.h = handle
        request.method = method

        self.dbg("Calling {} with handle {} Instance method {} with {} args".format(objtype, handle, method, len(args)))

        for arg in args:
# If we get to a default arg then no more args to pass
            if arg is Oasys.gRPC.defaultArg:
                break

# If the arg is a tuple then it must be the last arg (for varargs).
# If the length of the tuple is 0 then don't send it
            elif isinstance(arg, tuple) and len(arg) == 0:
                break

            self.add_request_arg(request, arg)

        response = self.stub.InstanceMethod(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK

# Decode the response value
        return self.decode_response_value(response.value)


    def classGetter(self, objtype, name):
# Getter
        request = Oasys.gRPC.oasys_pb2.ClassGetRequest()

        request.type     = objtype
        request.property = name

        self.dbg("Calling {} Class Getter with property {}".format(objtype, name))

        response = self.stub.ClassGet(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK

# Decode the response value
        return self.decode_response_value(response.value)


    def classSetter(self, objtype, name, value):
# Setter
        request = Oasys.gRPC.oasys_pb2.ClassSetRequest()

        request.type     = objtype
        request.property = name

        self.encode_request_value(request, value)

        self.dbg("Calling {} Class Setter with property {}={}".format(objtype, name, value))

        response = self.stub.ClassSet(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK


    def classMethod(self, objtype, method, *args):
# Class Method call
        request = Oasys.gRPC.oasys_pb2.ClassMethodRequest()

        request.type   = objtype
        request.method = method

        self.dbg("Calling {} Class method {} with {} args".format(objtype, method, len(args)))

        for arg in args:
# If we get to a default arg then no more args to pass
            if arg is Oasys.gRPC.defaultArg:
                break

# If the arg is a tuple then it must be the last arg (for varargs).
# If the length of the tuple is 0 then don't send it
            elif isinstance(arg, tuple) and len(arg) == 0:
                break

            self.add_request_arg(request, arg)

        response = self.stub.ClassMethod(request)
        self.dbg("Returned {} '{}'".format(response.status, response.message))

        assert response.status == Oasys.gRPC.oasys_pb2.STATUS_OK

# Decode the response value
        return self.decode_response_value(response.value)


    def finalise(self):
# Finalise
        noarg = Oasys.gRPC.oasys_pb2.NoArg()
        self.dbg("Calling Finalise")
        response = self.stub.Finalise(noarg)
        self.dbg("Returned {} '{}'".format(response.status, response.message))
        self.stub    = None
        self.channel = None


    def terminate(self):
# Close connection and terminate process
        noarg = Oasys.gRPC.oasys_pb2.NoArg()
        self.dbg("Calling Terminate")
        response = self.stub.Exit(noarg)
        self.dbg("Returned {} '{}'".format(response.status, response.message))
        self.stub    = None
        self.channel = None


    def add_request_arg(self, request, arg):
# Add an argument to the gRPC request
# The request can have multiple arguments
        oneof = request.args.add()

        if arg is None:
            oneof.nullarg.n = True
        elif isinstance(arg, bool):
            oneof.boolarg.b = arg
        elif isinstance(arg, int):
            oneof.intarg.i = arg
        elif isinstance(arg, float):
            oneof.dblarg.d = arg
        elif isinstance(arg, str):
            oneof.strarg.s = arg
        elif isinstance(arg, dict):
            for key in arg:
                self.dbg("dict {}={} ({})".format(key, arg[key], type(arg[key])))
                if arg[key] is None:
                    oneof.dictarg.d[key].nullarg.n = True
                elif isinstance(arg[key], bool):
                    oneof.dictarg.d[key].boolarg.b = arg[key]
                elif isinstance(arg[key], int):
                    oneof.dictarg.d[key].intarg.i = arg[key]
                elif isinstance(arg[key], float):
                    oneof.dictarg.d[key].dblarg.d = arg[key]
                elif isinstance(arg[key], str):
                    oneof.dictarg.d[key].strarg.s = arg[key]
                elif isinstance(arg[key], Oasys.gRPC.OasysItem):
                    oneof.dictarg.d[key].itemarg.t = arg[key]._objtype
                    oneof.dictarg.d[key].itemarg.h = arg[key]._handle
                else:
                    raise NotImplementedError("Unsupported dict type {}".format(type(arg[key])))
        elif isinstance(arg, list):
            for index in range(len(arg)):
                self.dbg("list {}={} ({})".format(index, arg[index], type(arg[index])))

                value = oneof.listarg.values.add()

                if arg[index] is None:
                    value.nullarg.n = True
                elif isinstance(arg[index], bool):
                    value.boolarg.b = arg[index]
                elif isinstance(arg[index], int):
                    value.intarg.i = arg[index]
                elif isinstance(arg[index], float):
                    value.dblarg.d = arg[index]
                elif isinstance(arg[index], str):
                    value.strarg.s = arg[index]
                elif isinstance(arg[index], Oasys.gRPC.OasysItem):
                    value.itemarg.t = arg[index]._objtype
                    value.itemarg.h = arg[index]._handle
                else:
                    raise NotImplementedError("Unsupported list type {}".format(type(arg[index])))
        elif isinstance(arg, tuple):    # Tuples used for varargs
            for index in range(len(arg)):
                self.dbg("tuple {}={} ({})".format(index, arg[index], type(arg[index])))

                value = oneof.listarg.values.add()

                if arg[index] is None:
                    value.nullarg.n = True
                elif isinstance(arg[index], bool):
                    value.boolarg.b = arg[index]
                elif isinstance(arg[index], int):
                    value.intarg.i = arg[index]
                elif isinstance(arg[index], float):
                    value.dblarg.d = arg[index]
                elif isinstance(arg[index], str):
                    value.strarg.s = arg[index]
                elif isinstance(arg[index], Oasys.gRPC.OasysItem):
                    value.itemarg.t = arg[index]._objtype
                    value.itemarg.h = arg[index]._handle
                else:
                    raise NotImplementedError("Unsupported tuple type {}".format(type(arg[index])))
        elif isinstance(arg, Oasys.gRPC.OasysItem):
            oneof.itemarg.t = arg._objtype
            oneof.itemarg.h = arg._handle
        else:
            raise NotImplementedError("Unsupported type {}".format(type(arg)))


    def encode_request_value(self, request, value):
# Encode the value that we want to set in the class/instance setter
# for the gRPC request
        if value is None:
            request.value.nullarg.n = True
        elif isinstance(value, bool):
            request.value.boolarg.b = value
        elif isinstance(value, int):
            request.value.intarg.i = value
        elif isinstance(value, float):
            request.value.dblarg.d = value
        elif isinstance(value, str):
            request.value.strarg.s = value
        elif isinstance(value, Oasys.gRPC.OasysItem):
            request.value.itemarg.t = value._objtype
            request.value.itemarg.h = value._handle
        else:
            raise NotImplementedError("Unsupported type {}".format(type(arg)))
        


    def decode_response_value(self, response_value):
# Decode a response value from a gRPC call depending on the type
        if response_value.HasField("boolarg"):
            self.dbg("Bool value {}".format(response_value.boolarg.b))
            return response_value.boolarg.b
        elif response_value.HasField("intarg"):
            self.dbg("Integer value {}".format(response_value.intarg.i))
            return response_value.intarg.i
        elif response_value.HasField("dblarg"):
            self.dbg("Double value {}".format(response_value.dblarg.d))
            return response_value.dblarg.d
        elif response_value.HasField("strarg"):
            self.dbg("String value '{}'".format(response_value.strarg.s))
            return response_value.strarg.s
        elif response_value.HasField("nullarg"):
            self.dbg("Null value")
            return None
        elif response_value.HasField("dictarg"):
            self.dbg("Dict value")
            d = {}
            for key in response_value.dictarg.d:
                if response_value.dictarg.d[key].HasField("boolarg"):
                    d[key] = response_value.dictarg.d[key].boolarg.b
                    self.dbg("  '{}'={} (bool)".format(key, response_value.dictarg.d[key].boolarg.b))
                elif response_value.dictarg.d[key].HasField("intarg"):
                    d[key] = response_value.dictarg.d[key].intarg.i
                    self.dbg("  '{}'={} (int)".format(key, response_value.dictarg.d[key].intarg.i))
                elif response_value.dictarg.d[key].HasField("dblarg"):
                    d[key] = response_value.dictarg.d[key].dblarg.d
                    self.dbg("  '{}'={} (double)".format(key, response_value.dictarg.d[key].dblarg.d))
                elif response_value.dictarg.d[key].HasField("strarg"):
                    d[key] = response_value.dictarg.d[key].strarg.s
                    self.dbg("  '{}'={} (string)".format(key, response_value.dictarg.d[key].strarg.s))
                elif response_value.dictarg.d[key].HasField("nullarg"):
                    d[key] = None
                    self.dbg("  '{}'=None (None)".format(key))
                elif response_value.dictarg.d[key].HasField("itemarg"):
                    d[key] = self.decode_itemarg(response_value.dictarg.d[key].itemarg)
                    self.dbg("  '{}' (item)".format(key))
                else:
                    raise NotImplementedError("Unsupported type for dict {} arg".format(key))
            return d
        elif response_value.HasField("listarg"):
            self.dbg("List value")
            l = []
            for value in response_value.listarg.values:
                if value.HasField("boolarg"):
                    l.append(value.boolarg.b)
                    self.dbg("  '{}'={} (bool)".format(len(l), value.boolarg.b))
                elif value.HasField("intarg"):
                    l.append(value.intarg.i)
                    self.dbg("  '{}'={} (int)".format(len(l), value.intarg.i))
                elif value.HasField("dblarg"):
                    l.append(value.dblarg.d)
                    self.dbg("  '{}'={} (double)".format(len(l), value.dblarg.d))
                elif value.HasField("strarg"):
                    l.append(value.strarg.s)
                    self.dbg("  '{}'={} (string)".format(len(l), value.strarg.s))
                elif value.HasField("nullarg"):
                    l.append(None)
                    self.dbg("  '{}'=None (None)".format(len(l)))
                elif value.HasField("itemarg"):
                    l.append(self.decode_itemarg(value.itemarg))
                    self.dbg("  '{}' (item)".format(len(l)))
                else:
                    raise NotImplementedError("Unsupported type for list arg {}".format(len(l)))
            return l
        elif response_value.HasField("itemarg"):
            return self.decode_itemarg(response_value.itemarg)

        raise NotImplementedError("Unsupported type")


    def decode_itemarg(self, itemarg):
# Decode an itemarg response value
        self.dbg("Item value type {} handle {}".format(itemarg.t, itemarg.h))

        if self.program == "PRIMER":
            import Oasys.PRIMER
            return Oasys.PRIMER.createInstance(itemarg.t, itemarg.h)
        elif self.program == "D3PLOT":
            import Oasys.D3PLOT
            return Oasys.D3PLOT.createInstance(itemarg.t, itemarg.h)
        elif self.program == "T/HIS":
            import Oasys.THIS
            return Oasys.THIS.createInstance(itemarg.t, itemarg.h)
        elif self.program == "REPORTER":
            import Oasys.REPORTER
            return Oasys.REPORTER.createInstance(itemarg.t, itemarg.h)

        raise NotImplementedError("Unknown program")

    def dbg(self, message):
# Print debug messages if enabled

        if not self.debug:
            return

        print(message)
