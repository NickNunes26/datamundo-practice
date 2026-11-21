-- English semantic / i18n views over the raw Portuguese TechStore tables.
-- Keeps seed_techstore.sql untouched as the raw source layer while exposing
-- English table names, column names, and categorical labels for reporting.

CREATE OR REPLACE VIEW products AS
SELECT
    id,
    nome AS name,
    CASE categoria
        WHEN 'Notebooks'   THEN 'Laptops'
        WHEN 'Smartphones' THEN 'Smartphones'
        WHEN 'Monitores'   THEN 'Monitors'
        WHEN 'Tablets'     THEN 'Tablets'
        WHEN 'Acessorios'  THEN 'Accessories'
        ELSE categoria
    END AS category,
    preco AS price,
    custo AS cost,
    estoque AS stock
FROM produtos;

CREATE OR REPLACE VIEW customers AS
SELECT
    id,
    nome AS name,
    email,
    cidade AS city,
    estado AS state,
    data_cadastro AS signup_date,
    CASE segmento
        WHEN 'varejo'      THEN 'Retail'
        WHEN 'corporativo' THEN 'Corporate'
        WHEN 'governo'     THEN 'Government'
        ELSE segmento
    END AS segment
FROM clientes;

CREATE OR REPLACE VIEW sales_reps AS
SELECT
    id,
    nome AS name,
    CASE regiao
        WHEN 'Sudeste'      THEN 'Southeast'
        WHEN 'Sul'          THEN 'South'
        WHEN 'Nordeste'     THEN 'Northeast'
        WHEN 'Norte'        THEN 'North'
        WHEN 'Centro-Oeste' THEN 'Center-West'
        ELSE regiao
    END AS region,
    data_contratacao AS hire_date,
    meta_mensal AS monthly_target
FROM vendedores;

CREATE OR REPLACE VIEW orders AS
SELECT
    id,
    cliente_id AS customer_id,
    vendedor_id AS sales_rep_id,
    data_pedido AS order_date,
    CASE status
        WHEN 'entregue'    THEN 'Delivered'
        WHEN 'em_transito' THEN 'In Transit'
        WHEN 'pendente'    THEN 'Pending'
        WHEN 'cancelado'   THEN 'Cancelled'
        ELSE status
    END AS status,
    valor_total AS total_amount,
    desconto AS discount_pct,
    CASE forma_pagamento
        WHEN 'cartao' THEN 'Card'
        WHEN 'boleto' THEN 'Bank Slip'
        WHEN 'pix'    THEN 'Instant Transfer'
        ELSE forma_pagamento
    END AS payment_method
FROM pedidos;

CREATE OR REPLACE VIEW order_items AS
SELECT
    id,
    pedido_id AS order_id,
    produto_id AS product_id,
    quantidade AS quantity,
    preco_unitario AS unit_price
FROM itens_pedido;
