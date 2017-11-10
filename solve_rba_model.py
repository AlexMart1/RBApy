"""Solve standard RBA problem."""

# python 2/3 compatibility
from __future__ import division, print_function

# global imports
import sys
import os.path

# package imports
import rba


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide path to directory containing xml files.')
    else:
        xml_dir = sys.argv[1]
        if len(sys.argv) >= 3:
            medium = sys.argv[2]
        else:
            medium = 'default'

        model = rba.RbaModel.from_xml(xml_dir)
        results = model.solve(medium)
        # write results to file
        with open(os.path.join(xml_dir, 'reactions.out'), 'w') as f:
            f.write('Reaction\tFlux\n')
            for reaction, flux in results.reaction_fluxes().items():
                f.write('{}\t{}\n'.format(reaction, flux))
        with open(os.path.join(xml_dir, 'enzymes.out'), 'w') as f:
            f.write('Enzyme\tConcentration\n')
            for enzyme, conc in results.enzyme_concentrations().items():
                f.write('{}\t{}\n'.format(enzyme, conc))
        with open(os.path.join(xml_dir, 'process_machineries.out'), 'w') as f:
            f.write('Process\tMachinery Concentration\n')
            for process, conc in \
                    results.process_machinery_concentrations().items():
                f.write('{}\t{}\n'.format(process, conc))
        # write main transport reactions
        print('\nTop 10 boundary fluxes:')
        b_fluxes = results.sorted_boundary_fluxes()
        for flux in b_fluxes[:10]:
            print('{} {}'.format(*flux))
