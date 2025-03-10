from rankine import rankine

def main():
    # Cycle 1: Saturated vapor at turbine inlet
    cycle1 = rankine(p_low=8, p_high=8000, t_high=None, name='Rankine Cycle - Saturated')
    cycle1.calc_efficiency()
    cycle1.print_summary()
    print("\n" + "="*50 + "\n")

    # Cycle 2: Superheated at T1 = 1.7 * Tsat
    tsat = 295.06  # From saturated table at 8000 kPa
    t_high = 1.7 * tsat  # ≈ 501.6 °C
    cycle2 = rankine(p_low=8, p_high=8000, t_high=t_high, name='Rankine Cycle - Superheated')
    cycle2.calc_efficiency()
    cycle2.print_summary()

if __name__ == "__main__":
    main()