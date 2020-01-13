#import sqlite3

def join_sql():
    #We'll use firelynx's tables:
    presidents = pd.DataFrame({"name": ["Bush", "Obama", "Trump"],
                               "president_id":[43, 44, 45]})
    terms = pd.DataFrame({'start_date': pd.date_range('2001-01-20', periods=5, freq='48M'),
                          'end_date': pd.date_range('2005-01-21', periods=5, freq='48M'),
                          'president_id': [43, 43, 44, 44, 45]})
    war_declarations = pd.DataFrame({"date": [dt.datetime(2001, 9, 14), dt.datetime(2003, 3, 3), dt.datetime(2017, 3, 3)],
                                     "name": ["War in Afghanistan", "Iraq War", "New"]})
    
    #return terms#war_declarations
    
    #Make the db in memory
    conn = sqlite3.connect(':memory:')
    #write the tables
    terms.to_sql('terms', conn, index=False)
    presidents.to_sql('presidents', conn, index=False)
    war_declarations.to_sql('wars', conn, index=False)

    qry = '''
        select  
            start_date PresTermStart,
            end_date PresTermEnd,
            wars.date WarStart,
            presidents.name Pres
        from
            terms left join wars on
            date between start_date and end_date join presidents on
            terms.president_id = presidents.president_id
        '''
    
    qry = """
            select a.*, b.name, b.date
                from terms as a left join wars as b
                where a.start_date <= b.date and b.date <= a.end_date
            """
    
    df = pd.read_sql_query(qry, conn)
    conn.close()
    
    return df