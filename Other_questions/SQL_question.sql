------

SELECT
    t.date AS date_commande,
    SUM(t.prod_price * t.prod_qty) AS chiffre_affaires
FROM TRANSACTIONS t
WHERE t.date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY t.date
ORDER BY t.date ASC;

------


SELECT
    t.client_id AS client,
    SUM(CASE WHEN p.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
    SUM(CASE WHEN p.product_type = 'DECO'   THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM TRANSACTIONS t
JOIN PRODUCT_NOMENCLATURE p
    ON t.prod_id = p.product_id
WHERE t.date BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY t.client_id
ORDER BY t.client_id ASC;
