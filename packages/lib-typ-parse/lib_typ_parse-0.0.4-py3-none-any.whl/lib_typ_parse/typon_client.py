import os
import requests
import lib_typ_parse.parse.parse_skeleton as parse_skeleton
import lib_typ_parse.parse.parse_L0_skeleton as parse_L0_skeleton

# algorithm:
# 1.) invoke service endpoint
# 2.) perform commands to complete operation

# write {out_dir}/{exe_name}.cpp and compile to {out_dir}/{exe_name}.exe; compilation done on client side
# serviceEndpoint = (http|https)://[ipAddr]:[portNum]
# req: { module_L0_skeleton, target_module, module_dir, out_dir, exe_name }
# return { cpp_repr, compilation_cmd } or { error : [traceback] }
def compileCpp(serviceEndpoint, api_key, target_module, module_dir, out_dir, exe_name, printProg=True):
    # module_L0_skeleton = parse_skeleton.read_absolute_skeleton(target_module, module_dir)
    module_L0_skeleton = parse_L0_skeleton.select_code_skeletons(target_module, module_dir)
    # print(module_L0_skeleton)
    # print(module_L0_skeleton['drivers.cache_server_driver']['#namespace_mapping'])

    O1 = [ 'api_key', 'module_L0_skeleton', 'target_module', 'module_dir', 'out_dir', 'exe_name' ]
    O2 = [ api_key, module_L0_skeleton, target_module, module_dir, out_dir, exe_name ]
    pl = {
        O1[i] : O2[i]
        for i in range(0, len(O1))
    }

    url = f'{serviceEndpoint}/getSource'
    # oRepr = repr(pl)
    resp = requests.post(url, json=pl)
    respJson = resp.json()

    if 'error' in respJson:
        print('error occurred:')
        print()
        print(respJson['error'])
        return

    cpp_repr = respJson['cpp_repr']
    compilation_cmd = respJson['compilation_cmd']
    full_cmd = f'cd {out_dir} && {compilation_cmd}'
    # print(cpp_repr)
    # print(compilation_cmd)

    cpp_path = f'{out_dir}/{exe_name}.cpp'
    exe_path = f'{out_dir}/{exe_name}.exe'
    # print(cpp_path)
    fp = open(cpp_path, 'w')
    fp.write(cpp_repr)
    fp.close()

    if printProg:
        print(f'wrote cpp source into: {cpp_path}')
        print('compiling source locally')

    op_result = os.system(full_cmd)

    if printProg:
        print('finished compiling locally')
        print(f'wrote exe source into: {exe_path}')

    return [respJson, op_result]

# write to {out_dir}/{exe_name}.exe; compilation done on server side
# serviceEndpoint = (http|https)://[ipAddr]:[portNum]
# read request from binary form
# req: { module_L0_skeleton, target_module, module_dir, out_dir, exe_name }
# return { exe_repr, op_result } or { error : [traceback] }
def compileExe(serviceEndpoint, api_key, target_module, module_dir, out_dir, exe_name, printProg=True):
    module_L0_skeleton = parse_skeleton.read_absolute_skeleton(target_module, module_dir)
    O1 = [ 'api_key', 'module_L0_skeleton', 'target_module', 'module_dir', 'out_dir', 'exe_name' ]
    O2 = [ api_key, module_L0_skeleton, target_module, module_dir, out_dir, exe_name ]
    pl = {
        O1[i] : O2[i]
        for i in range(0, len(O1))
    }

    if printProg:
        print('retrieving executable repr')

    url = f'{serviceEndpoint}/getExe'
    resp = requests.post(url, json=pl)
    respJson = eval(resp.content)
    # print(respJson['exe_repr'])
    # return
    # respJson = resp.json()

    if 'error' in respJson:
        print('error occurred:')
        print()
        print(respJson['error'])
        return

    exe_repr = respJson['exe_repr']
    # b1 = isinstance(exe_repr, bytes)
    # print(b1)
    exe_path = f'{out_dir}/{exe_name}.exe'
    fp = open(exe_path, 'wb')
    fp.write(exe_repr)
    fp.close()

    if printProg:
        print(f'wrote exe source into: {exe_path}')

    return respJson
