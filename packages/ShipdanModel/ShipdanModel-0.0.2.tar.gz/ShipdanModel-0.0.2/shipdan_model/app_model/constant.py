class DietPaymentScheduleStatus:
    UNDEFINED = 0
    REGISTERED = 1
    DIET_CREATE_COMPLETE = 2
    DIET_CREATE_FAILED = 3
    PAYMENT_COMPLETE = 4
    PAYMENT_FAILED = 5
    SKIP = 6
    PAYMENT_CANCEL = 7
    CANCEL = -1


DIET_PAYMENT_SCHEDULE_STATUS = (
    (DietPaymentScheduleStatus.UNDEFINED, '미정'),
    (DietPaymentScheduleStatus.REGISTERED, '등록'),
    (DietPaymentScheduleStatus.DIET_CREATE_COMPLETE, '식단 생성 성공'),
    (DietPaymentScheduleStatus.DIET_CREATE_FAILED, '식단 생성 실패'),
    (DietPaymentScheduleStatus.PAYMENT_COMPLETE, '결제 성공'),
    (DietPaymentScheduleStatus.PAYMENT_FAILED, '결제 실패'),
    (DietPaymentScheduleStatus.SKIP, '건너뜀'),
    (DietPaymentScheduleStatus.PAYMENT_CANCEL, '결제 취소'),
    (DietPaymentScheduleStatus.CANCEL, '해지'),
)