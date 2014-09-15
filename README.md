orngutan-test
=============

package orngutan and provide more functionality. Orangutan test will collect logs every three scripts.


Environment Setup
-----------------
Setup environment for oranugutan test
```
$ python setup.py install
```

Execution
---------
To run the script, you'll need to modify ```config/template.json``` to setup your environment. If you have no idea about what to fill, you can reference ```config/flame_config.json```.

### Generate Scripts
```
$ python lib/gen_randomsc.py --config config/template.json
```
or, give the parameters directly
```
$ python lib/gen_randomsc.py --gen_scripts_amount 10 --gen_scripts_steps 10000 --gen_scripts_output scripts/sample/
```

### Execution
To start orangutan test, use the command:
```
$ python lib/runner.py --config config/template.json
```
Or generate random script by giving ```--gen-scripts True```
```
$ python lib/runner.py --gen-scripts True --config config/template.json
```

