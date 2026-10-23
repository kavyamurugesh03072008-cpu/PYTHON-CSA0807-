BEGIN
    total ← 0

    FOR day ← 1 TO 10 DO
        INPUT litres, fat, snf

        IF litres > 0 AND fat >= 0 AND snf >= 0 THEN
            fat_steps ← ROUND((fat - 3.5) / 0.1)
            snf_steps ← ROUND((snf - 8.5) / 0.1)

            rate ← 30 + (fat_steps × 0.40)
                       + (snf_steps × 0.30)

            payment ← ROUND(litres × rate, 2)
            total ← total + payment

            OUTPUT payment
        ELSE
            OUTPUT "Invalid entry"
        END IF
    END FOR

    OUTPUT total
END
