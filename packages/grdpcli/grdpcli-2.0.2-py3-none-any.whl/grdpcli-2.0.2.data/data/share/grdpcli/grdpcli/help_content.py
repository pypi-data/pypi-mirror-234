# GRDP CLI Usage

`grdp [command] [subcommand]`

Commands:
- `pods`                                                                                     List of pods
- `services`                                                                                 List of services
- `ingress`                                                                                  List of ingress
- `pvc`                                                                                      List of volumes
- `exec`                                                                                     Join to pod or exec command inside a pod
- `logs`                                                                                     Logs of selected pod
- `pf`                                                                                       PortForwarding from pod to localhost

## Examples:
- `$ grdp`                                                                                   Configure grdp-cli
- `$ grdp help`                                                                              Show this help message
- `$ grdp all`                                                                               Show all resources
- `$ grdp pods`                                                                              Show list of pods
- `$ grdp services`                                                                          Show list of application services
- `$ grdp ingress`                                                                           Show list of ingresses and DNS names
- `$ grdp pvc`                                                                               Show persistent volumes
- `$ grdp logs`                                                                              Show list of pods to view logs
- `$ grdp logs nginx-7db9fccd9b-bx4cv --folow`                                               Show logs with specifying a pod name: `nginx-7db9fccd9b-bx4cv` - pod name. Option --folow
- `$ grdp exec`                                                                              Show list of pods to join inside
- `$ grdp exec nginx-7db9fccd9b-bx4cv "ls -la"`                                              Exec command inside pod. Where: `nginx-7db9fccd9b-bx4cv` - pod name, `"ls -la"` - bash command
- `$ grdp pf --pod nginx-7db9fccd9b-bx4cv --pod-port 80 --local-port 8080 --ip 127.0.0.1`    Portforward port from pod to localhost.

Other commands:
- `$ grdp --help`                                                                            Show this help message
- `$ grdp --version`                                                                         Show version
- `$ grdp --no-browser`                                                                      Authorization without a browser, via console
- `$ grdp --print-kubectl-config`                                                            Print kubectl config
