def test_example():
    # it is awkward if the README.md example does not work

    from dicomselect import Database
    from pathlib import Path

    db_path = Path('tests/output/example.db')
    db_path.parent.mkdir(exist_ok=True)

    # initialize the Database object with a path to the to-be-created SQLite database file
    db = Database(db_path)

    # create the .db file, using test data as the input directory.
    db.create('tests/input/ProstateX', max_workers=4)

    with (db as query):
        # we only want to convert images with patient_id "ProstateX-0000" and image_direction "transverse"
        query_0000 = query.where('patient_id', '=', 'ProstateX-0000'
                                 ).where('image_direction', '=', 'transverse')

        # print out a detailed extraction of our query
        print(query_0000.info())

    # initialize the Plan object, with a template of DICOM headers for our conversion
    # (note: dcm to dcm conversion is possible, if you only need restructuring of your data)
    plan = db.plan('{patient_id}/prostateX_{series_description}_{instance_creation_time}', query_0000)

    target_dir = Path('tests/output/example')
    if target_dir.exists():
        import shutil
        shutil.rmtree(target_dir)

    # ensure these properties are set
    plan.target_dir = 'tests/output/example'
    plan.extension = '.mha'
    plan.max_workers = 4

    # print out a detailed structure of our intended conversion
    print(plan.to_string())

    plan.execute()
    # check out the result in 'tests/output/example'!
