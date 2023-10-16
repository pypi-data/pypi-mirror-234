import cdxg
from cdxg.logging import log
# from wfs.utils.common import get_results


class Assertion(cdxg.TestCase):

    def assert_equals_results(self, case, testcase, gtext, aresults, exresults, stepline, gtitems):
        # print(aresults, exresults, gtext, gtitems)
        # reportpath, features, ustory, teststeps, testdata, depend, tdata = gtitems
        if gtext == aresults:
            '''if depend != 'Y':
                get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                            exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
            log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
            self.assertEqual(aresults, gtext)
            log.success('Expected Results :' + str(exresults))
        elif aresults is None:
            log.success('Expected Results :' + str(exresults))
        else:
            # gexpected = aresults.split('*')
            # print(gexpected, gtext)
            if gtext in aresults:
                '''if depend != 'Y':
                    get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                                exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
                log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
                self.assertIn(gtext, aresults)
            else:
                '''if depend != 'Y':
                    get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                                exresults, results='FAILED', fontx='FC2C03', sshots=features, incidentids=None)'''
                log.error('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ': FAIL')
                self.assertEqual(aresults, gtext)
                log.error('Expected Results :' + str(exresults))

    def assert_not_equals_results(self, case, testcase, gtext, aresults, exresults, stepline, gtitems):
        # reportpath, features, ustory, teststeps, testdata, depend, tdata = gtitems
        if gtext == aresults:
            '''get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                        exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
            log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
            self.assertNotEqual(aresults, gtext)
            log.success('Expected Results :' + str(exresults))
        elif aresults is None:
            log.success('Expected Results :' + str(exresults))
        else:
            '''get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                        exresults, results='FAILED', fontx='FC2C03', sshots=None, incidentids=None)'''
            log.error('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ': FAIL')
            self.assertNotEqual(aresults, gtext)
            log.error('Expected Results :' + str(exresults))

    def assert_in_results(self, case, testcase, gtext, aresults, exresults, stepline, gtitems):
        # print(case, testcase, gtext, aresults, exresults, stepline, gtitems)
        # reportpath, features, ustory, teststeps, testdata, depend, tdata = gtitems
        if aresults in gtext:
            '''if depend != 'Y':
                get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                            exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
            log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
            self.assertIn(aresults, gtext)
            log.success('Expected Results :' + str(exresults))
        elif aresults is None:
            log.success('Expected Results :' + str(exresults))
        else:
            if type(gtext) == list:
                glen = len(aresults)
                for xlen in range(0, glen):
                    if aresults[xlen] in gtext:
                        '''if depend != 'Y':
                            get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                                        exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
                        if xlen == 0:
                            log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
                            log.success('Expected Results :' + str(exresults))
                        self.assertIn(aresults[xlen], gtext)
                    else:
                        '''if depend != 'Y':
                            get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                                        exresults, results='FAILED', fontx='FC2C03', sshots=features, incidentids=None)'''
                        log.error('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ': FAIL')
                        self.assertIn(aresults[xlen], gtext)
                        log.error('Expected Results :' + str(exresults))
            else:
                '''get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                            exresults, results='FAILED', fontx='FC2C03', sshots=features, incidentids=None)'''
                log.error('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ': FAIL')
                self.assertIn(aresults, gtext)
                log.error('Expected Results :' + str(exresults))

    def assert_not_in_results(self, case, testcase, gtext, aresults, exresults, stepline, gtitems):
        # reportpath, features, ustory, teststeps, testdata, depend, tdata = gtitems
        if aresults not in gtext:
            '''get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                        exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=None)'''
            log.success('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ' PASS')
            self.assertNotIn(aresults, gtext)
            log.success('Expected Results :' + str(exresults))
        elif aresults is None:
            log.success('Expected Results :' + str(exresults))
        else:
            '''get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults,
                        exresults, results='FAILED', fontx='FC2C03', sshots=None, incidentids=None)'''
            log.error('CASE[' + str(case) + '] ' + str(testcase) + '-' + str(stepline) + ': FAIL')
            self.assertNotIn(aresults, gtext)
            log.error('Expected Results :' + str(exresults))
