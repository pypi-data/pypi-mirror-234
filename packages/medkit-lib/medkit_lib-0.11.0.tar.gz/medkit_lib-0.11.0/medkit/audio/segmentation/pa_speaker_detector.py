"""
This module needs extra-dependencies that are not installed with medkit.
To install them, use :
`pip install torch https://github.com/pyannote/pyannote-audio/archive/refs/tags/JSALT2023.tar.gz`.
"""

__all__ = ["PASpeakerDetector"]

from pathlib import Path
from typing import Dict, Iterator, List, Optional, Union
from typing_extensions import Literal

# When pyannote and spacy are both installed, a conflict might occur between the
# ujson library used by pandas (a pyannote dependency) and the ujson library used
# by srsrly (a spacy dependency), especially in docker environments.
# srsly seems to end up using the ujson library from pandas, which is older and does not
# support the escape_forward_slashes parameters, instead of its own.
# The bug seems to only happen when pandas is imported from pyannote, not if
# we import pandas manually first.
# So as a workaround, we always import pandas before importing something from pyannote
import pandas  # noqa: F401
from pyannote.audio.pipelines import SpeakerDiarization
import torch

from medkit.core import Attribute
from medkit.core.audio import SegmentationOperation, Segment, Span


class PASpeakerDetector(SegmentationOperation):
    """Speaker diarization operation relying on `pyannote.audio`

    Each input segment will be split into several sub-segments corresponding
    to speech turn, and an attribute will be attached to each of these sub-segments
    indicating the speaker of the turn.

    `PASpeakerDetector` uses the `SpeakerDiarization` pipeline from
    `pyannote.audio`, which performs the following steps:

    - perform multi-speaker VAD with a `PyanNet` segmentation model and extract \
    voiced segments ;

    - compute embeddings for each voiced segment with a \
    embeddings model (typically speechbrain ECAPA-TDNN) ;

    - group voice segments by speakers using a clustering algorithm such as
      agglomerative clustering, HMM, etc.

    """

    def __init__(
        self,
        segmentation_model: Union[str, Path],
        embedding_model: Union[str, Path],
        clustering: Literal[
            "AgglomerativeClustering",
            "FINCHClustering",
            "HiddenMarkovModelClustering",
            "OracleClustering",
        ],
        output_label: str,
        pipeline_params: Optional[Dict] = None,
        min_nb_speakers: Optional[int] = None,
        max_nb_speakers: Optional[int] = None,
        segmentation_batch_size: int = 1,
        embedding_batch_size: int = 1,
        uid: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        segmentation_model:
            Name (on the HuggingFace models hub) or path of the `PyanNet`
            segmentation model. When a path, should point to the .bin file
            containing the model.
        embedding_model:
            Name (on the HuggingFace models hub) or path to the embedding model.
            When a path to a speechbrain model, should point to the directory containing
            the model weights and hyperparameters.
        clustering:
            Clustering method to use.
        output_label:
            Label of generated turn segments.
        pipeline_params:
            Dictionary of segmentation and clustering parameters. The dictionary
            can hold a "segmentation" key and a "clustering" key pointing to
            sub dictionaries. Refer to the pyannote documentation for the
            supported parameters segmentation and clustering parameters
            (clustering parameters depend on the clustering method used).
        min_nb_speakers:
            Minimum number of speakers expected to be found.
        max_nb_speakers:
            Maximum number of speakers expected to be found.
        segmentation_batch_size:
            Number of input segments in batches processed by segmentation model.
        embedding_batch_size:
            Number of pre-segmented audios in batches processed by embedding model.
        uid:
            Identifier of the detector.
        """

        # Pass all arguments to super (remove self)
        init_args = locals()
        init_args.pop("self")
        super().__init__(**init_args)

        self.output_label = output_label
        self.min_nb_speakers = min_nb_speakers
        self.max_nb_speakers = max_nb_speakers

        self._pipeline = SpeakerDiarization(
            segmentation=str(segmentation_model),
            embedding=str(embedding_model),
            clustering=clustering,
            embedding_exclude_overlap=True,
            segmentation_batch_size=segmentation_batch_size,
            embedding_batch_size=embedding_batch_size,
        )
        self._pipeline.instantiate(pipeline_params)

    def run(self, segments: List[Segment]) -> List[Segment]:
        """Return all turn segments detected for all input `segments`.

        Parameters
        ----------
        segments:
            Audio segments on which to perform diarization.

        Returns
        -------
        List[~medkit.core.audio.Segment]:
            Segments detected as containing speech activity (with speaker
            attributes)
        """
        return [
            turn_seg
            for seg in segments
            for turn_seg in self._detect_turns_in_segment(seg)
        ]

    def _detect_turns_in_segment(self, segment: Segment) -> Iterator[Segment]:
        audio = segment.audio
        file = {
            "waveform": torch.from_numpy(audio.read()),
            "sample_rate": audio.sample_rate,
        }

        diarization = self._pipeline.apply(
            file,
            min_speakers=self.min_nb_speakers,
            max_speakers=self.max_nb_speakers,
        )

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # trim original audio to turn start/end points
            turn_audio = audio.trim_duration(turn.start, turn.end)

            turn_span = Span(
                start=segment.span.start + turn.start,
                end=segment.span.start + turn.end,
            )
            speaker_attr = Attribute(label="speaker", value=speaker)
            turn_segment = Segment(
                label=self.output_label,
                span=turn_span,
                audio=turn_audio,
                attrs=[speaker_attr],
            )

            if self._prov_tracer is not None:
                self._prov_tracer.add_prov(turn_segment, self.description, [segment])
                self._prov_tracer.add_prov(speaker_attr, self.description, [segment])

            yield turn_segment
