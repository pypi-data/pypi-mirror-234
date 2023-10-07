.. _noise2read-documentation:

.. image:: ./logo/logo.svg
   :align: center
   :target: https://noise2read.readthedocs.io/en/latest/

.. image:: https://readthedocs.org/projects/noise2read/badge/?version=latest
    :target: https://noise2read.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Turn 'noise' to signal: accurately rectify millions of erroneous short reads through graph learning on edit distances
=====================================================================================================================

`noise2read <https://noise2read.readthedocs.io/en/latest/>`_, originated in a computable rule translated from PCR erring mechanism that: a rare read is erroneous if it has a neighboring read of high abundance, turns erroneous reads into their original state without bringing up any non-existing sequences into the short read set(&lt 300bp) including DNA and RNA sequencing (DNA/RNA-seq), small RNA, unique molecular identifiers (UMI) and amplicon sequencing data.

Click `noise2read <https://noise2read.readthedocs.io/en/latest/>`_ to jump to its documentation
===============================================================================================

**Note**: All the experimental results obtained in this study utilised version 0.2.7 of noise2read.

Quick-run example
=================

Quick-run example for testing `noise2read <https://noise2read.readthedocs.io/en/latest/>`__ by setting only 1 trial for Optuna and 10 estimators for xGboost which are not the parameters used in our paper.

* `noise2read <https://noise2read.readthedocs.io/en/latest/>`_ installation
   
Please refer to `QuickStart <https://noise2read.readthedocs.io/en/latest/QuickStart.html>`_ or `Installation <https://noise2read.readthedocs.io/en/latest/Usage/Installation.html>`_.

* Clone the codes with datasets in github

.. code-block:: console

    git clone https://github.com/Jappy0/noise2read
    cd noise2read/Examples/simulated_miRNAs

* Quick-run testing `noise2read <https://noise2read.readthedocs.io/en/latest/>`_ on D14

  * with high ambiguous errors correction and using GPU for training (running about 4 mins with 26 cores and GPU)

  .. code-block:: console

      noise2read -m correction -c ../../config/quick_test.ini -a True -g gpu_hist

Examples for correcting simulated miRNAs data with mimic UMIs by `noise2read <https://noise2read.readthedocs.io/en/latest/>`_
=============================================================================================================================

Take data sets `D14 and D16 <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/EqlRHFa57i1MmQa57cGoz_UBSmUqXYRrY0kUhYEGrciyZQ>`_ as examples.

* `noise2read <https://noise2read.readthedocs.io/en/latest/>`__ installation
   
Please refer to `QuickStart <https://noise2read.readthedocs.io/en/latest/QuickStart.html>`_ or `Installation <https://noise2read.readthedocs.io/en/latest/Usage/Installation.html>`_.

* Clone the codes with datasets in github

.. code-block:: console

    git clone https://github.com/Jappy0/noise2read
    cd noise2read/Examples/simulated_miRNAs

* Reproduce the evaluation results for D14 and D16 from raw, true and corrected datasets

.. code-block:: console

    noise2read -m evaluation -i ./raw/D14_umi_miRNA_mix.fa -t ./true/D14_umi_miRNA_mix.fa -r ./correct/D14_umi_miRNA_mix.fasta -d ./D14
    noise2read -m evaluation -i ./raw/D16_umi_miRNA_subs.fa -t ./true/D16_umi_miRNA_subs.fa -r ./correct/D16_umi_miRNA_subs.fasta -d ./D16

* **correcting D14**

  * with high ambiguous errors correction and using GPU for training 

  .. code-block:: console

      noise2read -m correction -c ./configs/D14.ini

  * without high ambiguous errors correction and using GPU for training 
  
  .. code-block:: console

      noise2read -m correction -c ./configs/D14_without_high.ini

* **correcting D16**

  * with high ambiguous errors correction and using GPU for training 

  .. code-block:: console

      noise2read -m correction -c ./configs/D16.ini

  * without high ambiguous errors correction and using GPU for training 

  .. code-block:: console

      noise2read -m correction -c ./configs/D16_without_high.ini

* **Expected Results**

Please find the expected log files and correction results at the folder noise2read of `benchmark <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/Eln7oX7Vv8lMhU8XSujBzjIBCjzD0rTPOsEO4uWTW0Bryw?e=6kEy3H>`_ for correcting data sets of D14-D16. The results under noise2read and noise2read-1 represent the corrected results with and without high ambiguous errors' prediction, respectively. 

  **Note**: Noise2read may produce slightly different corrected result from these results under Examples/simulated_miRNAs/correct and `correction <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/Eln7oX7Vv8lMhU8XSujBzjIBCjzD0rTPOsEO4uWTW0Bryw?e=6kEy3H>`_. This is because the easy-usable and automatic tuning of the classifiers' parameters facilitates wide-range explorations, different best models are obtained for each training, but the final prediction results are stable within a certain range. We have discussed this in the Discussion section of our paper. 

Examples for correcting outcome sequence of ABEs and CBEs by `noise2read <https://noise2read.readthedocs.io/en/latest/>`_
=========================================================================================================================

* Clone the codes

.. code-block:: console

    git clone https://github.com/Jappy0/noise2read
    cd noise2read/CaseStudies
    mkdir ABEs_CBEs
    cd ABEs_CBEs

* Download datasets under the folder of data of `D32_D33 <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/EokIIeQd2nFHjlpurzDaBywB7Smy6Sm0dBR86GIJt0PSdg?e=S6w34F>`_.

* Using `noise2read <https://noise2read.readthedocs.io/en/latest/>`_ to correct the datasets. The running time of each experiment is about 13 minutes using 26 cores and GPU for training.

.. code-block:: console

    noise2read -m correction -i ./data/D32_ABE_outcome_seqs.fasta -a False -d ./ABE/
    noise2read -m correction -i ./data/D33_CBE_outcome_seqs.fasta -a False -d ./CBE/

* **Expected Results**

Please find the expected log files and correction results at the folder `D32_D33 <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/EokIIeQd2nFHjlpurzDaBywB7Smy6Sm0dBR86GIJt0PSdg?e=S6w34F>`_. The results for correcting D32 and D33 are presented under the folders of ABE and CBE, respectively.

  **Note**: Noise2read may produce slightly different corrected result from these under D32_ABE and D33_CBE of `D32_D33 <https://studentutsedu-my.sharepoint.com/:f:/g/personal/pengyao_ping_student_uts_edu_au/EokIIeQd2nFHjlpurzDaBywB7Smy6Sm0dBR86GIJt0PSdg?e=S6w34F>`_. This is because the easy-usable and automatic tuning of the classifiers' parameters facilitates wide-range explorations, different best models are obtained for each training, but the final prediction results are stable within a certain range. We have discussed this in the Discussion section of our paper. 

More examples for reproducing our experiments in this paper can be found at the `Examples <https://noise2read.readthedocs.io/en/latest/Usage/Examples/Index.html>`_ of the documentation
========================================================================================================================================================================================

Feel free to contact me if you have any questions on running noise2read or are interested in noise2read.
========================================================================================================