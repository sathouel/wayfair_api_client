
class Queries:
    purchase_order_fields = '''
            {
                poNumber,
                poDate,
                estimatedShipDate,
                orderType,
                shippingInfo {
                    shipSpeed,
                    carrierCode
                },
                packingSlipUrl,
                products {
                    partNumber,
                    quantity,
                    price,
                },
                shipTo {
                    name,
                    address1,
                    address2,
                    address3,
                    city,
                    state,
                    country,
                    postalCode,
                    phoneNumber
                }
            }    
    '''
    purchase_order_list_query = '''
        query purchaseOrders($limit: Int!) {
            purchaseOrders(
                filters: [
                    {
                        field: open,
                        equals: "true"
                    }
                ],
                limit: $limit
            ) %s
        }
    ''' % purchase_order_fields

    purchase_order_query = '''
        query purchaseOrders($poNumber: String!) {
            purchaseOrders(
                filters: [
                    {
                        field: open,
                        equals: "true"
                    },
                    {
                        field: poNumber,
                        equals: $poNumber
                    }
                ]
            ) %s
        }
    ''' % purchase_order_fields