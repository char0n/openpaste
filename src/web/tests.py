import unittest
import models
import uuid
from difflib import unified_diff
from web.lib.vendor import patch
from StringIO import StringIO

class VisitorModelTest(unittest.TestCase):

    def test_attributes(self):
        visitor = models.Visitor()
        visitor.uuid = uuid.uuid4()
        visitor.attributes = {'property' : 'value'}
        visitor.save()

        loadVisitor = models.Visitor.objects.get(uuid__exact=visitor.uuid)

        self.assertEqual({"property": "value"}, loadVisitor.attributes)

class DiffTest(unittest.TestCase):

    def testDiff(self):
        version1 = StringIO()
        version1.writelines(["test 1\n", "test 2\n"])

        version2 = StringIO()
        version2.writelines(["test 1\n", "test 3"])


        udiff = ''.join(unified_diff(version1.getvalue().splitlines(True), version2.getvalue().splitlines(True),
                                    fromfile='1234', tofile='5678',
                                    fromfiledate='Sat Jan 26 23:30:50 1991',
                                    tofiledate='Fri Jun 06 10:20:52 2003'))

        expected = StringIO()
        expected.writelines([
            "--- 1234 Sat Jan 26 23:30:50 1991\n",
            "+++ 5678 Fri Jun 06 10:20:52 2003\n",
            "@@ -1,2 +1,2 @@\n",
            " test 1\n",
            "-test 2\n",
            "+test 3"
        ])

        self.assertEqual(expected.getvalue(), udiff)

    def testDiffNoLineEnd(self):
        version1 = StringIO()
        version1.writelines(["test 1\n", "test 2"])

        version2 = StringIO()
        version2.writelines(["test 1\n", "test 3"])


        udiff = ''.join(unified_diff(version1.getvalue().splitlines(True), version2.getvalue().splitlines(True),
                                    fromfile='1234', tofile='5678',
                                    fromfiledate='Sat Jan 26 23:30:50 1991',
                                    tofiledate='Fri Jun 06 10:20:52 2003'))

        expected = StringIO()
        expected.writelines([
            "--- 1234 Sat Jan 26 23:30:50 1991\n",
            "+++ 5678 Fri Jun 06 10:20:52 2003\n",
            "@@ -1,2 +1,2 @@\n",
            " test 1\n",
            "-test 2+test 3"
        ])
        self.assertEqual(expected.getvalue(), udiff)

class PatchTest(unittest.TestCase):

    def testPatch(self):
        version1 = StringIO()
        version1.writelines(["test 1\n", "test 2\n"])

        udiff = StringIO();
        udiff.writelines([
            "--- 1234 Sat Jan 26 23:30:50 1991\n",
            "+++ 5678 Fri Jun 06 10:20:52 2003\n",
            "@@ -1,2 +1,2 @@\n",
            " test 1\n",
            "-test 2\n",
            "+test 3"
        ])

        p = patch.fromstring(udiff.getvalue())
        patched = p.patch_stream(version1, p.hunks[0])

        expected = "test 1\ntest 3"

        self.assertEqual(expected, "".join(list(patched)))

    def testPatchNoLineEndInVersion1(self):
        version1 = StringIO()
        version1.writelines(["test 1\n", "test 2"])

        udiff = StringIO();
        udiff.writelines([
            "--- 1234 Sat Jan 26 23:30:50 1991\n",
            "+++ 5678 Fri Jun 06 10:20:52 2003\n",
            "@@ -1,2 +1,2 @@\n",
            " test 1\n",
            "-test 2+test 3\n",
        ])

        p = patch.fromstring(udiff.getvalue())

        self.assertEqual(0, len(p.hunks[0]))
