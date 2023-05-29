def parse_reg():
    f = open('APPS.reg', 'r', encoding='UTF-8')
    apps = []
    apps_folder = 'apps'
    for line in f:
        try:
            app_name = line.split(":")[0]
            app_class_name = line.split(":")[1].strip()
            module = __import__(apps_folder + '.' + app_name)
            app_file =  getattr(module, app_name)
            app = getattr(app_file, app_class_name)
            apps.append({'name':app_name, 'app':app})
        except Exception as e:
            print(e)
            continue
    return apps
