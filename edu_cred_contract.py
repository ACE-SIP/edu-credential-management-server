from pyteal import *


def approval_program():
    # Unsure syntax for Bytes parameter
    institution_key = Bytes("institution")
    eduCred_key = Bytes("eduCred_id")
    verifiableCred_key = Bytes("verifiableCred_id")
    applicant_key = Bytes("applicant")
    issuer_key = Bytes('issuer_key')

    @Subroutine(TealType.none)
    def permitCredentialsTo(assetID: Expr, account: Expr) -> Expr:
        asset_holding = AssetHolding.balance(Global.current_application_address(), assetID)
        return Seq(
            asset_holding,
            If(asset_holding.hasValue()).Then(
                Seq(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields(
                        {
                            TxnField.type_enum: TxnType.AssetTransfer,
                            TxnField.xfer_asset: assetID,
                            TxnField.asset_close_to: account,
                        }
                    ),
                    InnerTxnBuilder.Submit(),
                )
            ),
        )

    on_create = Seq(
        App.globalPut(institution_key, Txn.application_args[0]),
        App.globalPut(eduCred_key, Btoi(Txn.application_args[1])),
        App.globalPut(verifiableCred_key, Btoi(Txn.application_args[2])),
        App.globalPut(applicant_key, Global.zero_address()),
        Approve(),
    )

    # unsure function
    on_setup = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: App.globalGet(eduCred_key),
                TxnField.asset_receiver: Global.current_application_address(),
            }
        ),
        InnerTxnBuilder.Submit(),
        Approve(),
    )

    on_call_method = Txn.application_args[0]
    on_call = Cond([on_call_method == Bytes("setup"), on_setup])

    credential_holding = AssetHolding.balance(Global.current_application_address(), App.globalGet(eduCred_key))

    # credential transfer
    on_delete = Seq(
        If(App.globalGet(applicant_key) != Global.zero_address()).Then(
            Seq(
                If(credential_holding.hasValue())
                .Then(
                    # application valid
                    permitCredentialsTo(
                        App.globalGet(eduCred_key),
                        App.globalGet(applicant_key),
                    )
                )
                .Else(
                    Seq(
                        # application invalid
                        permitCredentialsTo(
                            App.globalGet(eduCred_key),
                            App.globalGet(issuer_key)
                        ),
                    )
                )
            )
            .Else(
                permitCredentialsTo(App.globalGet(eduCred_key), App.globalGet(issuer_key))
            ),
            Approve(),
        ),
        Reject(),
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [
            Txn.on_completion() == OnComplete.DeleteApplication,
            on_delete,
        ],
        [
            Or(
                Txn.on_completion() == OnComplete.OptIn,
                Txn.on_completion() == OnComplete.CloseOut,
                Txn.on_completion() == OnComplete.UpdateApplication,
            ),
            Reject(),
        ],
    )

    return program


def clear_state_program():
    return Approve()


if __name__ == "__main__":
    with open("auction_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("auction_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)
