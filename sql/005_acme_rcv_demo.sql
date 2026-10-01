-- ============================================================
-- VALORA
-- ACME Demo RCV Data
-- Period: January - December 2025
-- ALL DATA IS SIMULATED
-- ============================================================

do $$
declare
    acme_id uuid;
    month_num integer;
    transaction_num integer;
    doc_date date;
    net_amount numeric(18,2);
    iva_amount numeric(18,2);
begin

    -- Get ACME company ID
    select id into acme_id
    from public.companies
    where nombre_fantasia = 'ACME';

    if acme_id is null then
        raise exception 'ACME company not found';
    end if;


    -- ========================================================
    -- SALES
    -- Approximately 20 invoices per month
    -- ========================================================

    for month_num in 1..12 loop

        for transaction_num in 1..20 loop

            doc_date :=
                make_date(2025, month_num, 1)
                + ((transaction_num * 27) % 27);

            -- Simulated net sales: CLP 500,000 - 5,000,000
            net_amount :=
                500000
                + ((month_num * 317000
                + transaction_num * 421000) % 4500000);

            iva_amount := round(net_amount * 0.19);

            insert into public.rcv_ventas (
                company_id,
                periodo,
                tipo_documento,
                rut_cliente,
                razon_social,
                folio,
                fecha_documento,
                monto_exento,
                monto_neto,
                iva,
                monto_total
            )
            values (
                acme_id,
                '2025' || lpad(month_num::text, 2, '0'),
                33,
                case (transaction_num % 5)
                    when 0 then '76.111.111-1'
                    when 1 then '76.222.222-2'
                    when 2 then '76.333.333-3'
                    when 3 then '76.444.444-4'
                    else        '76.555.555-5'
                end,
                case (transaction_num % 5)
                    when 0 then 'Minería Norte SpA'
                    when 1 then 'Servicios Industriales Ltda.'
                    when 2 then 'Energía del Desierto SpA'
                    when 3 then 'Ingeniería Andina SpA'
                    else        'Procesos Industriales SpA'
                end,
                10000 + month_num * 100 + transaction_num,
                doc_date,
                0,
                net_amount,
                iva_amount,
                net_amount + iva_amount
            );

        end loop;

    end loop;


    -- ========================================================
    -- PURCHASES
    -- Approximately 12 invoices per month
    -- ========================================================

    for month_num in 1..12 loop

        for transaction_num in 1..12 loop

            doc_date :=
                make_date(2025, month_num, 1)
                + ((transaction_num * 19) % 27);

            -- Simulated net purchases: CLP 200,000 - 3,000,000
            net_amount :=
                200000
                + ((month_num * 211000
                + transaction_num * 293000) % 2800000);

            iva_amount := round(net_amount * 0.19);

            insert into public.rcv_compras (
                company_id,
                periodo,
                tipo_documento,
                tipo_compra,
                rut_proveedor,
                razon_social,
                folio,
                fecha_documento,
                monto_exento,
                monto_neto,
                iva_recuperable,
                iva_no_recuperable,
                monto_total
            )
            values (
                acme_id,
                '2025' || lpad(month_num::text, 2, '0'),
                33,
                'Del Giro',
                case (transaction_num % 5)
                    when 0 then '77.111.111-1'
                    when 1 then '77.222.222-2'
                    when 2 then '77.333.333-3'
                    when 3 then '77.444.444-4'
                    else        '77.555.555-5'
                end,
                case (transaction_num % 5)
                    when 0 then 'Tecnología Industrial SpA'
                    when 1 then 'Servicios Técnicos Norte Ltda.'
                    when 2 then 'Electrónica Industrial SpA'
                    when 3 then 'Comunicaciones Chile Ltda.'
                    else        'Suministros Industriales SpA'
                end,
                20000 + month_num * 100 + transaction_num,
                doc_date,
                0,
                net_amount,
                iva_amount,
                0,
                net_amount + iva_amount
            );

        end loop;

    end loop;

end $$;