class OperationResult:
    NO_OP = 'NO_OP'
    COMPLETED = 'COMPLETED'


class ApprovalStatuses:
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    APPROVAL_COMPLETED = 'APPROVAL_COMPLETED'
    REVERTED = 'REVERTED'
    REJECTED = 'REJECTED'


class ApprovalWorkflowTypes:
    class WB:
        TRADE_GRN = "TRD GRNs"
        STORAGE_TO_TRADE_GRN = "STT GRNs"
        WAREHOUSE_RECEIPT_GRN = "EWR GRNs"
        STORAGE_GRN = "STR GRNs"
        BROKER_PAYMENT_GRN = "BRP GRNs"
        LOAN_REPAYMENT_GRN = "LRP GRNs"
        CLIENT_DISPATCH = "Dispatches"
        PHYSICAL_DISPATCH = "Physical Dispatches"
        INTER_WAREHOUSE_DISPATCH = "ITW Dispatches"
        INTER_WAREHOUSE_LOGGING = "ITW Physical Dispatches"
        THIRD_PARTY_DISPATCH = "TP Dispatch"
        FIELD_CASH_PAYMENT = "Field Cash Payment"
        CASH_ADVANCE_REQUEST = "Cash Advance Request"
        LOAN = "Loan"
        OO_LOAN = "OOLoan"
        INPUT_SALE = "Input Sale"
        CSD_CIA_CONVERSION = "CSD-CIA Conversion"
        CIA_CSD_CONVERSION = "CIA-CSD Conversion"
        CLIENT_INVOICE = "Client Invoice"
        CLIENT_INVENTORY_SWAP = "Client inventory swap"
        OUTREACH_OFFICER_COMMISSION = "Outreach officer commission"
        MOISTURE_DATA = "Moisture data"
        FLOAT_REQUEST = "Float request"
        FLOAT_RETIREMENT = "Float retirement"
        JOURNAL_ENTRY = "Journal Entry"
        ALLOW_COOPERATIVE_FARMER_BOOK_LOAN_WHILE_OWNING = "Allow cooperative farmers book while owing"
        RE_BAGGING = "Re-bagging"
        SUSPENSE_ACCOUNT_TRANSACTIONS = "Suspense Account Transactions"
        UNALLOCATED_DISPATCH = "Unallocated Dispatch"
