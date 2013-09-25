for category in venues['response']['categories']:
    print category['name'] + ' ' + category['id']
    for sub_category in category['categories']:
            print '\t' + sub_category['name'] + ' ' + sub_category['id']
            for sub_sub_category in sub_category['categories']:
                    print '\t\t' + sub_sub_category['name'] + ' ' + sub_sub_category['id']