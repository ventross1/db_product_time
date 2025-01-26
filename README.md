# db_product_time
pokud db bude házet error 2013 (HY000): Lost connection to MySQL server during query
tak musíte zvýšit buď connect_timeout (v mém případě jsem zvýšil na 50) nebo max_allowed_packet ( v mém případě na 268 435 456 (256mb) nebo budete muset udělat obojí
