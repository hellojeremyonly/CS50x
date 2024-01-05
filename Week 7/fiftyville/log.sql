-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Searching for the crime scene reports on Humphrey Street
SELECT * FROM crime_scene_reports WHERE street = 'Humphrey Street';

-- Searching for the crime on the year, month and day
SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28;

-- Searching for license_plate of the car for reference
SELECT *  FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28;

-- Searching for clues in the interviews
SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day =28;

-- Searching the car license_plate through the bakery_security_logs
SELECT license_plate, COUNT(*) as visits FROM bakery_security_logs  WHERE year = 2023 AND month = 7 AND day = 28 GROUP BY license_plate HAVING visits > 1 ORDER BY visits DESC;

-- Searching for the car that drove away in the parking lot, finding out the bank transaction at that time and tracking the phone call made at the same time
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE activity = "exit" AND year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 40
)
AND phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
)
AND people.id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"
    )
);

-- Three names returned: 'Taylor', 'Diana' and 'Bruce' with their details (phone_number, passport_number, license_plate)
-- Tracing the phone calls made by the suspects to find the accomplices, if any
SELECT *
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
);

-- Again, three names returned: 'James', 'Philip' and 'Robin' together with their details as well
-- Now, we cross-references the call to determine who call who
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
AND receiver IN ("(676) 555-6554", "(725) 555-3243", "(375) 555-8161");

-- The result shows that 'Bruce' called 'Robin', 'Taylor' called 'James' and 'Diana' called 'Philip'
-- No luck here..
-- Moving on, we check the earliest flight tomorrow, as we gathered from the interviews that the suspect will be leaving the country
SELECT *
FROM flights
JOIN airports
ON airports.id = flights.origin_airport_id
WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND flights.hour BETWEEN 0 AND 12 AND airports.city = "Fiftyville"
ORDER BY flights.hour, flights.minute;

-- The flight results returned three flights departing at 8:20am (id4), 9:30am (id1) and 12:15pm (id11) respectively.
-- We then check the destination of the flights
SELECT full_name, city
FROM airports
WHERE id IN (1, 4, 11);

-- We have the destination of the flights: 'New York' (4), 'Chicago' (1) and 'San Francisco' (11).
-- We then check the six suspects and their passport to see if any their names is on the passenger list for the three flights
SELECT name, passport_number
FROM people
WHERE people.name IN ("Bruce", "Taylor", "Diana", "James", "Philip", "Robin")
AND passport_number IN (
    SELECT passport_number
    FROM passengers
    JOIN flights
    ON flights.id = passengers.flight_id
    JOIN airports
    ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND flights.hour BETWEEN 0 AND 12
    AND flights.origin_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city = "Fiftyville"
    )
    AND flights.destination_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city IN ("New York City", "Chicago", "San Francisco")
    )
);

-- Bingo! Two names returned: 'Taylor' and 'Diana' with their passport numbers
-- We now know that 'Taylor' and 'Diana' are the two suspects that will be leaving the country tomorrow
-- We then check the bank account of the two suspects to see if they have enough money to buy the flight tickets
SELECT full_name, city, passport_number, flights.destination_airport_id, flights.hour, flights.minute
FROM airports
JOIN flights
ON flights.origin_airport_id = airports.id
JOIN passengers
ON passengers.flight_id = flights.id
WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND hour BETWEEN 00 AND 12
AND passengers.passport_number IN (
    SELECT passport_number
    FROM people
    WHERE people.name IN ("Bruce", "Taylor", "Diana", "James", "Philip", "Robin")
);

-- The result shows that 'Taylor' and 'Diana' are on the flight passenger list to 'New York' at 8:20am
-- We shall do a cross-reference on the bank account transaction to determine who is the thief and who is the accomplice
SELECT name, atm_transactions.amount
FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw';

-- Result shows that 'Taylor' withdraw $60, 'Diana' withdraw $35 and 'Bruce' withdraw $50
-- Piece by piece, we know that 'Taylor' and 'Bruce' withdraw the most, and they are also on the same flights
-- From here, we are certain that one of them is the thief but we don't know who is the accomplices
-- shit, another dead end..
-- putting on detective hat.. let's think.. what did we miss out.. and we are doing the ideation now.. silence..
-- From the information, and a few round of "scissor, paper, stone", we can deduce that either both of them are involved or none of them are involved
-- If none or only one of them are involved, then the thief or accomplice must be "James" or "Robin", because they are not in the ATM transaction list

-- this is the final analysis
-- thief: 'Taylor' or 'Bruce' or either of them is thief and the other is accomplice
-- accomplice: 'James' or 'Robin' or either of them is accomplice and the other is thief
-- destination: 'New York'(This, we can be 100% sure)

-- Answer
-- thief: 'Bruce'
-- accomplice: 'Robin'
-- destination: 'New York' (8:20am)
