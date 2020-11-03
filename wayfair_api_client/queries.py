
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

    last_purchase_order_list_query = '''
        query purchaseOrders($limit: Int!) {
            purchaseOrders(
                limit: $limit,
                ordering: [
                    {
                        desc: "poDate"
                    }
                ]            
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

    accept_purchase_order_mutation = '''
    mutation acceptOrder($poNumber: String!, $shipSpeed: ShipSpeed!, $dryRun: Boolean!, $lineItems: [AcceptedLineItemInput!]!) {
        purchaseOrders {
            accept(
                poNumber: $poNumber,
                shipSpeed: $shipSpeed,
                dryRun: $dryRun,
                lineItems: $lineItems
            ) {
                id,
                handle,
                status,
                submittedAt,
                completedAt
            }
        }
    }    
    '''

    register_purchase_order = '''
    mutation register($params: RegistrationInput!) {
        purchaseOrders {
            register(
                registrationInput: $params
            ) {
                id,
                eventDate,
                pickupDate,
                poNumber
                consolidatedShippingLabel {
                    url
                }
                billOfLading {
                    url
                }
                generatedShippingLabels {
                    poNumber
                    fullPoNumber
                    carrier
                    carrierCode
                    trackingNumber
                }
                customsDocument {
                    required
                    url
                }
            }
        }
    }    
    '''

    inventory_mutation = """
    mutation save($inventory: [inventoryInput]!, $feed_kind: inventoryFeedKind!, $dry_run: Boolean!) {
        inventory {
            save(
                inventory: $inventory,
                feedKind: $feed_kind,
                dryRun: $dry_run
            ) {
                id,
                handle,
                status,
                submittedAt,
                completedAt
            }
        }
    }
    """    