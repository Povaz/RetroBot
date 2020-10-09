from season import Season

season = Season(9)

season.add_player('povaz')
season.add_player('sirio')

season.add_shortgame('Metroid', 'povaz')
season.add_shortgame('TLOZ', 'sirio')

season.add_mediumgame('Metroid2', 'povaz')
season.add_mediumgame('TLOZ2', 'sirio')

season.add_longgame('Metroid3', 'povaz')
season.add_longgame('TLOZ3', 'sirio')

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

season.easy_finished('TLOZ', 'povaz')
season.hard_finished('TLOZ2', 'povaz')

season.easy_finished('TLOZ', 'sirio')
season.hard_finished('TLOZ2', 'sirio')
season.challenge_completed('TLOZ2', 'sirio')

season.next_month()
season.winner('Metroid')