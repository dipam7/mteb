from __future__ import annotations

from mteb.abstasks.TaskMetadata import TaskMetadata

from ....abstasks import AbsTaskClassification


class YahooAnswersTopicsClassification(AbsTaskClassification):
    metadata = TaskMetadata(
        name="YahooAnswersTopicsClassification",
        description="Dataset composed of questions and answers from Yahoo Answers, categorized into topics.",
        reference="https://huggingface.co/datasets/yahoo_answers_topics",
        dataset={
            "path": "yahoo_answers_topics",
            "revision": "78fccffa043240c80e17a6b1da724f5a1057e8e5",
        },
        type="Classification",
        category="s2s",
        eval_splits=["test"],
        eval_langs=["eng-Latn"],
        main_score="accuracy",
        date=None,
        form=None,
        domains=["Web"],
        task_subtypes=None,
        license=None,
        socioeconomic_status=None,
        annotations_creators=None,
        dialect=None,
        text_creation=None,
        bibtex_citation=None,
        n_samples={"train": 1400000, "test": 60000},
        avg_character_length=None,
    )

    @property
    def metadata_dict(self) -> dict[str, str]:
        metadata_dict = dict(self.metadata)
        metadata_dict["n_experiments"] = 10
        metadata_dict["samples_per_label"] = 32
        return metadata_dict

    def dataset_transform(self):
        self.dataset = self.dataset.map(
            lambda examples: examples,
            remove_columns=["id", "question_title", "question_content"],
        )

        # doing it here so label remains of type ClassLabel
        self.dataset = self.dataset.rename_column("topic", "label")
        self.dataset = self.dataset.rename_column("best_answer", "text")

        self.dataset = self.dataset["test"].train_test_split(
            test_size=2048, train_size=2048, seed=42, stratify_by_column="label"
        )
