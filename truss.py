import os
import shutil

def removefile(path):
    if os.path.exists(path+"\\gengokit\\template\\NAME-service\\svc\\transport_http.gotemplate"):
        os.remove(path+"\\gengokit\\template\\NAME-service\\svc\\transport_http.gotemplate")
        print("success to remove transport_http.gotemplate\n")
    else:
        print("not file transport_http.gotemplate\n")

    if os.path.exists(path+"\\gengokit\\template\\template.go"):
        os.remove(path+"\\gengokit\\template\\template.go")
        print("success to remove template.go\n")
    else:
        print("not file template.go\n")

def removedir(path):
    try:
        shutil.rmtree(path+"\\gengokit\\template\\NAME-service\\svc\\client\\http")
    except :
        print("http_dir is removed\n")
    try:
        shutil.rmtree(path+"\\gengokit\\template\\NAME-service\\cmd")
    except :
        print("cmd is removed\n")


def updatefile(path):
    cli_file_context="""
package cli

    import (
        "{{.ImportPath -}} /svc/server"
    )

    var Config server.Config

    func init() {
            Config.GRPCAddr = "127.0.0.1:8888"
        }
    }
    """
    with open(path+"\\gengokit\\template\\NAME-service\\svc\\server\\cli\\cli.gotemplate","w") as cli:
        cli.write(cli_file_context)


    run_file_context="""
package server

    import (
        "log"
        "net"
        // 3d Party
        "google.golang.org/grpc"

        // This Service
        pb "{{.PBImportPath -}}"
        "{{.ImportPath -}} /svc"
        "{{.ImportPath -}} /handlers"
    )

    // Config contains the required fields for running a server
    type Config struct {
        GRPCAddr string
    }

    func NewEndpoints() svc.Endpoints {
        // Business domain.
        var service pb.{{.Service.Name}}Server
        {
            service = handlers.NewService()
            // Wrap Service with middlewares. See handlers/middlewares.go
            service = handlers.WrapService(service)
        }

        // Endpoint domain.
        var (
        {{range $i := .Service.Methods -}}
            {{ToLower $i.Name}}Endpoint = svc.Make{{$i.Name}}Endpoint(service)
        {{end}}
        )

        endpoints := svc.Endpoints{
        {{range $i := .Service.Methods -}}
            {{$i.Name}}Endpoint:    {{ToLower $i.Name}}Endpoint,
        {{end}}
        }

        // Wrap selected Endpoints with middlewares. See handlers/middlewares.go
        endpoints = handlers.WrapEndpoints(endpoints)

        return endpoints
    }

    // Run starts a new http server, gRPC server, and a debug server with the
    // passed config and logger
    func Run(cfg Config) {
        endpoints := NewEndpoints()

        // Mechanical domain.
        errc := make(chan error)

        // Interrupt handler.
        go handlers.InterruptHandler(errc)

        // gRPC transport.
        go func() {
            log.Println("transport", "gRPC","addr", cfg.GRPCAddr)
            ln, err := net.Listen("tcp", cfg.GRPCAddr)
            if err != nil {
                errc <- err
                return
            }

            srv := svc.MakeGRPCServer(endpoints)
            s := grpc.NewServer()
            pb.Register{{.Service.Name}}Server(s, srv)

            errc <- s.Serve(ln)
        }()

        // Run!
        log.Println("exit", <-errc)
    }
    """
    with open(path+"\\gengokit\\template\\NAME-service\\svc\\server\\run.gotemplate","w") as run_file:
        run_file.write(run_file_context)


def run(path):
    removedir(str)
    updatefile(str)
    removefile(str)
    os.startfile(str+"\\wininstall.bat")



str=input("input you truss absolute path:\n")
run(str)