# -*- coding: utf-8 -*-

import unittest
import logging
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BaseParallelTestCase import BaseParallelTestCase

__author__ = 'matth'

class ParallelManyThreadsAtSamePointTestNested(BaseParallelTestCase):

    def setUp(self):
        spec, subprocesses = self.load_workflow_spec(
            'Test-Workflows/Parallel-Many-Threads-At-Same-Point-Nested.bpmn20.xml',
            'Parallel Many Threads At Same Point Nested')
        self.workflow = BpmnWorkflow(spec, subprocesses)

    def test_depth_first(self):
        instructions = []
        for split1 in ['SP 1', 'SP 2']:
            for sp in ['A', 'B']:
                for split2 in ['1', '2']:
                    instructions.extend(split1 + sp + "|" + split2 + t for t in ['A', 'B'])
                    instructions.extend(
                        (
                            split1 + sp + "|" + 'Inner Done',
                            f"!{split1}{sp}|Inner Done",
                        )
                    )
                if sp == 'A':
                    instructions.append("!Outer Done")

            instructions.extend(('Outer Done', "!Outer Done"))
        logging.info('Doing test with instructions: %s', instructions)
        self._do_test(instructions, only_one_instance=False, save_restore=True)

    def test_breadth_first(self):
        instructions = []
        for t in ['A', 'B']:
            for split2 in ['1', '2']:
                for sp in ['A', 'B']:
                    instructions.extend(
                        split1 + sp + "|" + split2 + t
                        for split1 in ['SP 1', 'SP 2']
                    )
        for split1 in ['SP 1', 'SP 2']:
            for sp in ['A', 'B']:
                for _ in ['1', '2']:
                    instructions += [split1 + sp + "|" + 'Inner Done']

        for _ in ['SP 1', 'SP 2']:
            instructions += ['Outer Done']

        logging.info('Doing test with instructions: %s', instructions)
        self._do_test(instructions, only_one_instance=False, save_restore=True)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ParallelManyThreadsAtSamePointTestNested)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
