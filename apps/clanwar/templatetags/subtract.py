from django.template.defaultfilters import register

@register.filter(name='subtract')

def subtract(dic, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return dic[arg_list[0]] - dic[arg_list[1]]
