import demo_hic_et_nunc.models as models
from demo_hic_et_nunc.types.hen_minter.parameter.collect import Collect
from dipdup.models import HandlerContext, OperationContext


async def on_collect(
    ctx: HandlerContext,
    collect: OperationContext[Collect],
) -> None:
    swap = await models.Swap.filter(id=collect.parameter.swap_id).get()
    seller = await swap.creator
    buyer, _ = await models.Holder.get_or_create(address=collect.data.sender_address)

    trade = models.Trade(
        swap=swap,
        seller=seller,
        buyer=buyer,
        amount=int(collect.parameter.objkt_amount),
        level=collect.data.level,
        timestamp=collect.data.timestamp,
    )
    await trade.save()

    swap.amount_left -= int(collect.parameter.objkt_amount)  # type: ignore
    if swap.amount_left == 0:
        swap.status = models.SwapStatus.FINISHED
    await swap.save()