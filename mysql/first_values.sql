USE spa;

INSERT INTO room_type ( name, cost ) VALUES ( "Simple room", 5000 );
INSERT INTO room_type ( name, cost ) VALUES ( "Double room", 8000 );
INSERT INTO room_type ( name, cost ) VALUES ( "Standalone room", 12000 );
INSERT INTO room_type ( name, cost ) VALUES ( "Standalone vertical room", 12000 );
INSERT INTO room_type ( name, cost ) VALUES ( "Double vertical room", 8000 );

INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 2, 3, 10, 10 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 2, 3, 26, 10 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 10, 18 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 10, 26 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 10, 34 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 10, 42 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 10, 50 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 2, 10, 58 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 34, 18 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 34, 26 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 34, 34 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 34, 42 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 1, 1, 34, 50 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 5, 4, 34, 58 );

INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 3, 4, 10, 74 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 3, 5, 10, 90 );
INSERT INTO rooms ( room_type, number_of_windows, x, y ) VALUES ( 4, 5, 34, 82 );
