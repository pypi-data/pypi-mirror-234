from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from glob import glob
from re import compile

from eis1600.onomastics.re_pattern import SPELLING
from p_tqdm import p_uimap
from openiti.helper.ara import denormalize

from eis1600.gazetteers.Spellings import Spellings
from eis1600.gazetteers.Toponyms import Toponyms
from eis1600.helper.markdown_patterns import WORD
from eis1600.helper.repo import TRAINING_DATA_REPO
from eis1600.processing.preprocessing import get_tokens_and_tags, get_yml_and_miu_df
from eis1600.processing.postprocessing import reconstruct_miu_text_with_tags

place_terms = ['كورة', 'كور', 'قرية', 'قرى', 'مدينة', 'مدن', 'ناحية', 'نواح', 'نواحي', 'محلة', 'محلات', 'بلد', 'بلاد', 'ربع', 'ارباع', 'رستاق', 'رساتيق', 'أعمال']
technical_terms = ['من', 'بين',
                   'نسبة',
                   'يوم', 'يوما',
                   'مرحلة', 'مرحلتان', 'مرحلتين', 'مراحل',
                   'فرسخ', 'فرسخا', 'فراسخ',
                   'ميل', 'ميلا', 'أميال']
dn_pt = [denormalize(t) for t in place_terms]
dn_tt = [denormalize(t) for t in technical_terms]
dn_spelling = Spellings.instance().get_denormalized_list()
dn_toponyms = Toponyms.instance().total()

PLACES_REGEX = compile(r'(?:' + WORD + '(?: [،.():])?){1,7} (?:' + '|'.join(dn_pt) + r')(?:' + WORD + '،?){1,7}')
TT_REGEX = compile(r'|'.join(dn_pt + dn_tt + dn_spelling + dn_toponyms))


def annotate_miu(file: str) -> str:
    with open(file, 'r', encoding='utf-8') as miu_file_object:
        yml_handler, df = get_yml_and_miu_df(miu_file_object)

    write_out = False

    text = ' '.join(df['TOKENS'].loc[df['TOKENS'].notna()].to_list())
    text_updated = text

    if PLACES_REGEX.search(text_updated):
        m = PLACES_REGEX.search(text_updated)
        while m:
            start = m.start()
            end = m.end()
            if len(TT_REGEX.findall(m.group(0))) >= 3:
                write_out = True
                text_updated = text_updated[:start] + ' BTOPD ' + text_updated[start:end] + ' ETOPD ' + text_updated[end:]
                m = PLACES_REGEX.search(text_updated, end + 14)
            else:
                m = PLACES_REGEX.search(text_updated, end)

        if write_out:
            ar_tokens, tags = get_tokens_and_tags(text_updated.replace('  ', ' '))
            df.loc[df['TOKENS'].notna(), 'TAGS_LISTS'] = [[t] if t else t for t in tags]

            yml_handler.unset_reviewed()
            updated_text = reconstruct_miu_text_with_tags(df[['SECTIONS', 'TOKENS', 'TAGS_LISTS']])

            outpath = file.replace('5k_gold_standard', 'topo_descriptions')
            with open(outpath, 'w', encoding='utf-8') as ofh:
                ofh.write(str(yml_handler) + updated_text)

    return file


def main():
    arg_parser = ArgumentParser(
            prog=argv[0], formatter_class=RawDescriptionHelpFormatter,
            description='''Script to annotate onomastic information in gold-standard MIUs.'''
    )
    arg_parser.add_argument('-D', '--debug', action='store_true')

    args = arg_parser.parse_args()
    debug = args.debug

    infiles = glob(TRAINING_DATA_REPO + '5k_gold_standard/*.EIS1600')

    res = []
    if debug:
        for i, file in enumerate(infiles):
            print(i, file)
            res.append(annotate_miu(file))
    else:
        res += p_uimap(annotate_miu, infiles)

    print('Done')
