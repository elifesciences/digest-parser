# coding=utf-8

from collections import OrderedDict

EXPECTED = OrderedDict([
    ('id', u'99999'),
    ('title', u'Fishing for errors in the\xa0tests'),
    ('impactStatement', u'Testing a document which mimics the format of a file we’ve used  before plus CO<sub>2</sub> and Ca<sup>2+</sup>.'),
    ('published', '2018-08-01T00:00:00Z'),
    ('image', OrderedDict([
        ('thumbnail', OrderedDict([
            ('uri', 'https://iiif.elifesciences.org/digests/99999%2Fdigest-99999.jpg'),
            ('alt', ''),
            ('source', OrderedDict([
                ('mediaType', 'image/jpeg'),
                ('uri', 'https://iiif.elifesciences.org/digests/99999%2Fdigest-99999.jpg/full/full/0/default.jpg'),
                ('filename', 'digest-99999.jpg'),
                ])),
            ('size', OrderedDict([
                ('width', 0),
                ('height', 0)
                ])),
            ])),
        ])),
    ('subjects', [
        OrderedDict([
            ('id', 'biochemistry-chemical-biology'),
            ('name', 'Biochemistry and Chemical Biology'),
            ]),
        OrderedDict([
            ('id', 'structural-biology-molecular-biophysics'),
            ('name', 'Structural Biology and Molecular Biophysics'),
            ]),
        ]),
    ('content', [
        OrderedDict([
            ('type', 'paragraph'),
            ('text', u'Truely being able to recognize sample data is crucial for social interactions in humans. This is also added, CO<sub>2</sub> or Ca<sup>2+</sup>, &amp; 1 &lt; 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
            ]),
        OrderedDict([
            ('type', 'paragraph'),
            ('text', u'Some other mammals also identify sample data. For example, female medaka fish (<i>Oryzias latipes</i>) prefer sample data they have seen before to \u2018strangers\u2019. However, until now, it was not known if they can recognize individual faces, nor how they distinguish a specific male from many others.')
            ]),
        OrderedDict([
            ('type', 'image'),
            ('image', OrderedDict([
                ('uri', 'https://iiif.elifesciences.org/digests/99999%2Fdigest-99999.jpg'),
                ('alt', ''),
                ('source', OrderedDict([
                    ('mediaType', 'image/jpeg'),
                    ('uri', 'https://iiif.elifesciences.org/digests/99999%2Fdigest-99999.jpg/full/full/0/default.jpg'),
                    ('filename', 'digest-99999.jpg'),
                    ])),
                ('size', OrderedDict([
                    ('width', 0),
                    ('height', 0)
                    ])),
                ])),
            ('title', u'<b>It\u2019s not just mammals who can recognise sample data.</b>\u00a0Image credit:\u00a0Anonymous and Anonymous\u00a0(CC BY\u00a04.0)'),
        ]),
        OrderedDict([
            ('type', 'paragraph'),
            ('text', u'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?')
            ]),
        ]),
    ('relatedContent', [
        OrderedDict([
            ('type', 'research-article'),
            ('status', 'vor'),
            ('id', '99999'),
            ('version', 1),
            ('doi', '10.7554/eLife.99999'),
            ('authorLine', 'Anonymous et al.'),
            ('title', 'A research article related to the digest'),
            ('stage', 'published'),
            ('published', '2018-06-04T00:00:00Z'),
            ('statusDate', '2018-06-04T00:00:00Z'),
            ('volume', 7),
            ('elocationId', 'e99999')
            ])
        ]),
    ])
