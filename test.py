from season import Season

season = Season(9)

season.add_player(0, 'povaz')
season.add_player(1, 'sirio')

season.add_shortgame('Metroid', 0)
season.add_shortgame('TLOZ', 1)

season.add_mediumgame('Metroid2', 0)
season.add_mediumgame('TLOZ2', 1)

season.add_longgame('Metroid3', 0)
season.add_longgame('TLOZ3', 1)

season.add_easymode('Metroid', 'Finish the Game.')
season.add_hardmode('Metroid', 'Finish the Game without Save States')
season.add_challenge('Metroid', 'Finish the Game without Power Ups')

season.add_easymode('Metroid2', 'Finish the Game.')
season.add_hardmode('Metroid2', 'Finish the Game without Save States')
season.add_challenge('Metroid2', 'Finish the Game without Power Ups')

season.add_easymode('Metroid3', 'Finish the Game.')
season.add_hardmode('Metroid3', 'Finish the Game without Save States')
season.add_challenge('Metroid3', 'Finish the Game without Power Ups')

season.add_easymode('TLOZ', 'Finish the Game.')
season.add_hardmode('TLOZ', 'Finish the Game without Save States')
season.add_challenge('TLOZ', 'Finish the Game without Power Ups')

season.add_easymode('TLOZ2', 'Finish the Game.')
season.add_hardmode('TLOZ2', 'Finish the Game without Save States')
season.add_challenge('TLOZ2', 'Finish the Game without Power Ups')

season.add_easymode('TLOZ3', 'Finish the Game.')
season.add_hardmode('TLOZ3', 'Finish the Game without Save States')
season.add_challenge('TLOZ3', 'Finish the Game without Power Ups')

season.winner('TLOZ3')
season.winner('TLOZ2')
season.winner('TLOZ')

season.easy_finished('TLOZ', 0)
season.hard_finished('TLOZ2', 0)

season.easy_finished('TLOZ', 1)
season.hard_finished('TLOZ2', 1)
season.challenge_completed('TLOZ2', 1)

