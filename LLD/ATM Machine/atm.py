# # Design ATM Machine

# # Functional Requirements:- 
# # 1. If money in the bank it could be withdrawal else cannot be 
# # 2. Loading of money on ATM
# # 3. Isert card -> use pin validate card from bank and enter amount and allow wothdrawal of money
# # 4. Show no money in ATM In when there is no money
# # 5. Pin cannot be entered more then 3 times 
# #     Else card will will be blocked
# # 6. Reduce Money from bank accounts and ATM 
# # 7. Notify bank on Low money in ATM 
# # 8. Assuming only 1 bank
# # 9. Allow cancellation of Session at any time
# # 10. Send notification on money withdrawal
# # 11. Ensure card ejection on session cancellation

# # Non Functional Requirements:- 
# # 1. Be inherently secure
# # 2. Reciept Could be taken
# # 3. Balance Show Menu
# # 4. Allow multple cards per bank accounts
# # 5. Change Pin

# # Entities:-
# # ATM Machine
#     bank
#     atmId
#     slots: Multiple slots
#     slotWithdrawStrategy 
#     withdrawal -> Flow
#         -> Idle
#         -> Insert Card
#         -> Pin dal
#         -> Select Withdrawal
#         -> Put amount
#         -> Ensure ATM has money
#         -> Validate from bank
#         -> Run withdrawal strategy
#         -> End session
#     slotDeposit()

# # Card 
#     cardId
#     cardPin
#     cardCVV
#     cardExpiry
# # User
#     id
#     Name
#     attachedCards: [
#         Card
#     ]
# # Bank
#     # manages multiple accounts
#     - getBalance()
#     - withdrawMoney()
#     - verifyUser()
#     - depositMoney()
#     - notifyUser()

# NotificationChannel:
#     Mail
#     SMS
#     AppNotification
#     Chitthi

# BankNotification:
#     - channel    


# ATM Slots
#     -> deposit
#     -> Withdraw