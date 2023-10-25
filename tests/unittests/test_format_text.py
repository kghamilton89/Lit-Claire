import unittest
import random
import re

from utils.text import augmented_texts_generator, capitalize, USE_DASHES

class TestFormatText(unittest.TestCase):

    def normalize_text(self, text):
        return list(augmented_texts_generator(text, 0))[0]

    def test_augmentation(self):
        self.maxDiff = None

        keep_specials = False
        for use_line_breaks in False, True:

            B = "\n" if use_line_breaks else " "

            # Note: Ted is the one generated by names with the seed used below (random.seed(51))
            extreme_normalization = f"[Intervenant 1:] tu me fais rire je chante{B}[Intervenant 2:] il y a un bruit je l'ai dit à ted{B}[Intervenant 1:] ah"
            extreme_normalization2 = f"- tu me fais rire je chante{B}- il y a un bruit je l'ai dit à ted{B}- ah"

            for itest, (text, normalized_text, maximum) in enumerate([
                (
                    f"[Alison Jordy:] Tu me fais rire [LAUGHTER]. Je chante [SINGING]?{B}[claude-marie JR Michel:] Il y a un bruit [NOISE], je l'ai dit à [PII].{B}[Alison Jordy:] Ah",
                    f"[Alison Jordy:] Tu me fais rire [rire]. Je chante ?{B}[Claude-Marie JR Michel:] Il y a un bruit [bruit], je l'ai dit à [Nom].{B}[Alison Jordy:] Ah" if keep_specials else\
                    f"[Alison Jordy:] Tu me fais rire. Je chante ?{B}[Claude-Marie JR Michel:] Il y a un bruit, je l'ai dit à Ted.{B}[Alison Jordy:] Ah",
                    5 + 3 * USE_DASHES + (1 if keep_specials else 0),
                ),
                (
                    f"[Alison Jordy:] Tu me fais rire. Je chante ?{B}[claude-marie JR Michel:] Il y a un bruit, je l'ai dit à Ted.{B}[Alison Jordy:] Ah",
                    f"[Alison Jordy:] Tu me fais rire. Je chante ?{B}[Claude-Marie JR Michel:] Il y a un bruit, je l'ai dit à Ted.{B}[Alison Jordy:] Ah",
                    5 + 3 * USE_DASHES,
                ),
                (
                    f"[speaker001:] Tu me fais rire [LAUGHTER]. Je chante [SINGING]?{B}[speaker002:] Il y a un bruit [NOISE], je l'ai dit à [PII].{B}[speaker001:] Ah",
                    f"[Intervenant 1:] Tu me fais rire [rire]. Je chante ?{B}[Intervenant 2:] Il y a un bruit [bruit], je l'ai dit à [Nom].{B}[Intervenant 1:] Ah" if keep_specials else\
                    f"[Intervenant 1:] Tu me fais rire. Je chante ?{B}[Intervenant 2:] Il y a un bruit, je l'ai dit à Ted.{B}[Intervenant 1:] Ah",
                    5 + 3 * USE_DASHES + (1 if keep_specials else 0),
                ),
                (
                    f"[speaker001:] Tu me fais rire Je chante [SINGING]{B}[speaker002:] Il y a un bruit je l'ai dit à Ted{B}[speaker001:] Ah",
                    f"[Intervenant 1:] Tu me fais rire Je chante{B}[Intervenant 2:] Il y a un bruit je l'ai dit à Ted{B}[Intervenant 1:] Ah",
                    3 + 2 * USE_DASHES,
                ),
                (
                    f"[speaker001:] tu me fais rire. je chante [SINGING] ?{B}[speaker002:] il y a un bruit, je l'ai dit à ted{B}[speaker001:] ah",
                    f"[Intervenant 1:] tu me fais rire. je chante ?{B}[Intervenant 2:] il y a un bruit, je l'ai dit à ted{B}[Intervenant 1:] ah",
                    3 + 2 * USE_DASHES,
                ),
                (
                    f"[speaker001:] tu me fais rire je chante [SINGING]{B}[speaker002:] il y a un bruit je l'ai dit à ted{B}[speaker001:] ah",
                    f"[Intervenant 1:] tu me fais rire je chante{B}[Intervenant 2:] il y a un bruit je l'ai dit à ted{B}[Intervenant 1:] ah",
                    1 + 1 * USE_DASHES,
                ),
            ]):

                random.seed(51)
                all_variants = list(augmented_texts_generator(text, None))
                msg = f"\n{itest=}\n{maximum=}\n{text=}"
                self.assertEqual(len(all_variants)-1, maximum, msg=msg)               # Expected number of generated text
                self.assertEqual(len(all_variants), len(set(all_variants)), msg=msg)  # All generated texts are different
                self.assertEqual(all_variants[0], normalized_text, msg=msg)        # First text is the normalized text

                def custom_anonymize(text):
                    text2 = re.sub(r"(je l'ai dit à) [^\[]+(" + B + r"[\[\-])", r"\1 [PII]\2", text)
                    self.assertNotEqual(text2, text)
                    return text2

                for level in 5, 4, 3, 2, 1, 0:
                    
                    for force_augmentation in False, True,:

                        random.seed(51)
                        augmented_texts = list(augmented_texts_generator(text, level, force_augmentation=force_augmentation))
                        msg_augmented_texts= '\n----------\n'.join(augmented_texts)
                        msg = f"\n{itest=}\n{level=}\n{maximum=}\n{text=}\n<<<<<<<<<\naugmented_texts:\n{msg_augmented_texts}"
                        self.assertEqual(len(augmented_texts), min(maximum+1, level+1), msg=msg)    # Expected number of generated text
                        self.assertEqual(len(augmented_texts), len(set(augmented_texts)), msg=msg)  # All generated texts are different
                        if not force_augmentation or level > 0:
                            self.assertEqual(augmented_texts[0], normalized_text, msg=msg)              # First text is the normalized text
                        if level >= maximum:
                            # The deepest normalization is always in
                            self.assertTrue(extreme_normalization in augmented_texts, msg=msg + f"\n>>>>>>>>>\nNOT FOUND:\n{extreme_normalization}")
                            if USE_DASHES:
                                self.assertTrue(extreme_normalization2 in augmented_texts, msg=msg + f"\n>>>>>>>>>\nNOT FOUND:\n{extreme_normalization2}")
                        for t in augmented_texts:
                            self.assertTrue(t in all_variants, msg=msg + f"\n>>>>>>>>>\nNOT FOUND:\n{t}") # All generated texts are in the list of all variants

                normalized_text2 = custom_anonymize(normalized_text)

                # No augmentation
                random.seed(51)
                not_augmented_texts = list(augmented_texts_generator(text, 0, force_augmentation=False))
                self.assertEqual(len(not_augmented_texts), 1)
                not_augmented_texts2 = [custom_anonymize(t) for t in not_augmented_texts]
                self.assertEqual(not_augmented_texts2, [normalized_text2])

                # One augmented (or not) variant only
                found_augmented = False
                for _ in range(3):
                    augmented_texts = list(augmented_texts_generator(text, 0, force_augmentation=True))
                    self.assertEqual(len(augmented_texts), 1)
                    augmented_texts2 = [custom_anonymize(t) for t in augmented_texts]
                    if augmented_texts2[0] != normalized_text2:
                        found_augmented = True
                        break
                    msg = f"\n{itest=}\n{level=}\n{maximum=}\n{text=}\n<<<<<<<<<\naugmented texts:\n{augmented_texts2[0]}\n>>>>>>>>>\nnormalized text:\n{normalized_text2}"

                self.assertTrue(found_augmented, msg=msg) # The generated text can be different than the (normalized) text

            # Check unanomization (sometimes first names alone, sometimes first and last names)
            text = f"[speaker001:] A{B}[speaker002:] B{B}[speaker001:] C{B}[speaker003:] D{B}[speaker002:] E{B}[speaker003:] F{B}[speaker001:] G"
            random.seed(123)

            augmented_texts = []
            for i in range(3):
                augmented_texts += augmented_texts_generator(text, 4)

            # print(sorted(list(set(augmented_texts))))
            self.assertEqual(
                sorted(list(set(augmented_texts))),
                [
                f'[Elizabeth Neal:] A{B}[Susan Davis:] B{B}[Elizabeth Neal:] C{B}[Michael Rottenberg:] D{B}[Susan Davis:] E{B}[Michael Rottenberg:] F{B}[Elizabeth Neal:] G',
                f'[Elizabeth Neal:] a{B}[Susan Davis:] b{B}[Elizabeth Neal:] c{B}[Michael Rottenberg:] d{B}[Susan Davis:] e{B}[Michael Rottenberg:] f{B}[Elizabeth Neal:] g',
                f'[Intervenant 1:] A{B}[Intervenant 2:] B{B}[Intervenant 1:] C{B}[Intervenant 3:] D{B}[Intervenant 2:] E{B}[Intervenant 3:] F{B}[Intervenant 1:] G',
                f'[Intervenant 1:] a{B}[Intervenant 2:] b{B}[Intervenant 1:] c{B}[Intervenant 3:] d{B}[Intervenant 2:] e{B}[Intervenant 3:] f{B}[Intervenant 1:] g',
                f'[Jerome:] A{B}[Margaret:] B{B}[Jerome:] C{B}[Kevin:] D{B}[Margaret:] E{B}[Kevin:] F{B}[Jerome:] G',
                f'[Jerome:] a{B}[Margaret:] b{B}[Jerome:] c{B}[Kevin:] d{B}[Margaret:] e{B}[Kevin:] f{B}[Jerome:] g',
                f'[William:] A{B}[April:] B{B}[William:] C{B}[William:] D{B}[April:] E{B}[William:] F{B}[William:] G',
                f'[William:] a{B}[April:] b{B}[William:] c{B}[William:] d{B}[April:] e{B}[William:] f{B}[William:] g']
            )

            text = f"[Jean:] A{B}[Paul:] B{B}[Jean-Paul:] C{B}"
            augmented_texts = list(augmented_texts_generator(text, None))
            # print(sorted(list(set(augmented_texts))))
            self.assertEqual(
                sorted(list(set(augmented_texts))),
                [f'[Intervenant 1:] A{B}[Intervenant 2:] B{B}[Intervenant 3:] C',
                 f'[Intervenant 1:] a{B}[Intervenant 2:] b{B}[Intervenant 3:] c',
                 f'[Jean:] A{B}[Paul:] B{B}[Jean-Paul:] C',
                 f'[Jean:] a{B}[Paul:] b{B}[Jean-Paul:] c']
            ) # No dash when more than 2 speakers

            text = f"[Jean:] a"
            augmented_texts = list(augmented_texts_generator(text, None))
            # print(sorted(list(set(augmented_texts))))
            self.assertEqual(
                sorted(list(set(augmented_texts))),
                ['[Intervenant 1:] a',
                 '[Jean:] a',
                 'a']
            ) # No dash when 1 speaker

    def test_capitalize(self):

        self.assertEqual(
            capitalize("jean Jean JEAN JR jean-claude Jean-Claude d'estaing D'Estaing"),
            "Jean Jean Jean JR Jean-Claude Jean-Claude D'Estaing D'Estaing"
        )

    def test_remove_empty_turns(self):
        self.maxDiff = None

        for use_line_breaks in False, True:

            B = "\n" if use_line_breaks else " "

            text = f"[speaker001:] Je veux dire que Jean-Paul{B}[speaker002:] [rire]{B}[speaker001:] que tu ne peux pas{B}[speaker002:] que je ne peux pas ?...{B}[speaker001:] te moquer de moi comme ça! [spkeaker002:] ...{B}[speaker001:] Bah oui{B}[speaker002:] ..."
            normed_text = self.normalize_text(text)
            self.assertEqual(normed_text,
                f"[Intervenant 1:] Je veux dire que Jean-Paul que tu ne peux pas{B}[Intervenant 2:] que je ne peux pas ?...{B}[Intervenant 1:] te moquer de moi comme ça! Bah oui{B}[Intervenant 2:] ...")


            text = f"[M. Jean-Marie:] Hey{B}[Dr. Docteur JR:] Ow{B}[M. Jean-Marie:] [blah].{B}[M. Hide:] Hey{B}[M. Jean-Marie:] [re]{B}[m. hide:] Ow"
            normed_text = self.normalize_text(text)
            self.assertEqual(normed_text,
                f"[M. Jean-Marie:] Hey{B}[Dr. Docteur JR:] Ow{B}[M. Hide:] Hey Ow"
            )
