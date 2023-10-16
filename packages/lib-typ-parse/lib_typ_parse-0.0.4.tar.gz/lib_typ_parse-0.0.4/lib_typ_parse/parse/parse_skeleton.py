import json
import lib_typ_parse.helper.type_resolver as type_resolver
import lib_typ_parse.parse.parse_L0_skeleton as parse_L0_skeleton

def select_reverse_imports_map(skeleton):
    reverse_imports_map = {
        module_name : {
            skeleton[module_name]['imports']['alias_map'][module_alias] : module_alias
            for module_alias in skeleton[module_name]['imports']['alias_map']
        }
        for module_name in skeleton
        if len(module_name) > 0 and module_name[0] != '#'
    }
    return reverse_imports_map

def map_rel_type( abs_type, module_name, reverse_imports_map ):
    target_module, type_name = type_resolver.compute_relative_type(abs_type, module_name, reverse_imports_map)
    return type_resolver.reduce_rel_type( target_module, module_name, type_name, reverse_imports_map )

def condense_fxn(fxn_def, module_name, reverse_imports_map):
    result = {
        'fparam_ids' : fxn_def['fparam_ids'],
    }
    result['arguments'] = [ map_rel_type( abs_type, module_name, reverse_imports_map ) for abs_type in fxn_def['arguments'] ]
    result['return_type'] = map_rel_type( fxn_def['return_type'], module_name, reverse_imports_map )
    return result

def condense_class(class_def, module_name, reverse_imports_map):
    result = {
        'inherits' : class_def['inherits'],
        'functions' : {
            fxn_name : condense_fxn( class_def['functions'][fxn_name], module_name, reverse_imports_map )
            for fxn_name in class_def['functions'] if fxn_name[0] != '#'
        },
        'members' : {
            member_name : {
                'type' : map_rel_type( class_def['members'][member_name]['type'], module_name, reverse_imports_map )
            }
            for member_name in class_def['members'] if member_name[0] != '#'
        },
        'constructors' : [
            [
                [ identifier, map_rel_type( typon_type, module_name, reverse_imports_map ) ]
                for identifier, typon_type in constructor
            ]
            for constructor in class_def['constructors']
        ],
        'destructors' : [
            [
                [ identifier, map_rel_type( typon_type, module_name, reverse_imports_map ) ]
                for identifier, typon_type in destructor
            ]
            for destructor in class_def['destructors']
        ]
    }
    return result

def read_absolute_skeleton(target_module, module_dir):
    return parse_L0_skeleton.select_code_skeletons(target_module, module_dir)

def read_relative_skeleton(target_module, module_dir):
    skeleton = parse_L0_skeleton.select_code_skeletons(target_module, module_dir)
    reverse_imports_map = select_reverse_imports_map(skeleton)

    rel_skeleton = {
        module_name : {
            'imports_map' : skeleton[module_name]['imports']['alias_map'],
            'classes' : {
                class_name : condense_class( skeleton[module_name]['classes'][class_name], module_name, reverse_imports_map )
                for class_name in skeleton[module_name]['classes'] if len(class_name) > 0 and class_name[0] != '#'
            },
            'functions' : {
                fxn_name : condense_fxn( skeleton[module_name]['functions'][fxn_name], module_name, reverse_imports_map )
                for fxn_name in skeleton[module_name]['functions'] if len(fxn_name) > 0 and fxn_name[0] != '#'
            }
        }
        for module_name in skeleton if len(module_name) > 0 and module_name[0] != '#'
    }
    return rel_skeleton


def p1():
    target_module = 'image_upload.image_io'
    module_dir = '/home/algorithmspath/sdev/hb_api_typon/api'
    rel_skeleton = read_relative_skeleton(target_module, module_dir)
    S1 = json.dumps(rel_skeleton, indent=4)
    print(S1)

def main():
    p1()
    pass

if __name__ == '__main__':
    main()
