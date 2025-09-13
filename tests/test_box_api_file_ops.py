import os
import tempfile

import pytest
from box_sdk_gen import BoxClient, UploadFileAttributes, UploadFileAttributesParentField

from box_ai_agents_toolkit import box_file_text_extract

from .conftest import TestData


def test_box_upload_file(box_client_ccg: BoxClient):
    """Test uploading a file to Box"""
    # Test content
    test_content = "This is a test file created by the test_box_upload_file test."
    test_filename = "test_upload.txt"

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        # Upload to root folder
        with open(temp_file_path, "rb") as file:
            upload_attributes = UploadFileAttributes(
                name=test_filename, parent=UploadFileAttributesParentField(id="0")
            )
            upload_result = box_client_ccg.uploads.upload_file(upload_attributes, file)
            file_id = upload_result.entries[0].id

            # Verify file exists in Box
            file_info = box_client_ccg.files.get_file_by_id(file_id)
            assert file_info is not None
            assert file_info.name == test_filename

    finally:
        # Clean up - delete the test file from Box
        if "file_id" in locals():
            box_client_ccg.files.delete_file_by_id(file_id)

        # Delete local temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_box_download_file(box_client_ccg: BoxClient):
    """Test downloading a file from Box"""
    # First upload a file to test downloading
    test_content = "This is a test file for download testing."
    test_filename = "test_download.txt"

    # Upload to root folder
    upload_attributes = UploadFileAttributes(
        name=test_filename, parent=UploadFileAttributesParentField(id="0")
    )

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as file:
            upload_result = box_client_ccg.uploads.upload_file(upload_attributes, file)
            file_id = upload_result.entries[0].id

        # Test downloading
        download_stream = box_client_ccg.downloads.download_file(file_id)
        # Use read() instead of trying to access .content
        downloaded_data = download_stream.read()
        downloaded_content = downloaded_data.decode("utf-8")
        assert downloaded_content == test_content

    finally:
        # Clean up - delete the test file from Box
        if "file_id" in locals():
            box_client_ccg.files.delete_file_by_id(file_id)

        # Delete local temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_text_box_extracted_text(
    box_client_ccg: BoxClient, text_extract_test_files: TestData
):
    # Ensure we have a test template to work with
    if not text_extract_test_files.test_files:
        pytest.skip("No test templates available for Doc Gen batch creation.")

    # get the id of the docx file form list
    hab_docx_file_id = ""
    img_file_id = ""
    test_docx_file_id = ""

    for f in text_extract_test_files.test_files:
        if f.name:
            if f.name.endswith("1-01.docx"):
                hab_docx_file_id = f.id
            if f.name.endswith(".png"):
                img_file_id = f.id
            if f.name.endswith("test.docx"):
                test_docx_file_id = f.id

    assert hab_docx_file_id != "", "No .docx file found in test files"
    docx_representation = box_file_text_extract(
        client=box_client_ccg, file_id=hab_docx_file_id
    )

    # Expected text in the docx file
    # {'content': 'SCHIAPARELLI PLAZA PROPERTY LEASE AGREEMENT\nThis Lunar Property Lease Agreement (hereinafter referred to as the "Agreement") is made and entered into on this 4/24/24 by and between:\n\nLessor: Schiaparelli plaza, with a registered address at Schiaparelli crater, Oceanus Procellarum, Moon, hereinafter referred to as the "Lessor."\n\nLessee: Marie Tharp, with a registered address marie.tharp@moonhabitat.space, hereinafter referred to as the "Lessee."\n\nBoth parties agree to the following terms and conditions governing the lease of lunar property located in the designated lunar territory as described below.\n1. PROPERTY DESCRIPTION\nThe Lessor agrees to lease to the Lessee a designated Sigle unit in Communal Dome of lunar surface, identified as HAB-1-01, on the Schiaparelli Plaza Property.\nBEDROOMS:\nA large, private bedroom fitted with temperature-controlled walls and soft lunar lighting, ensuring a comfortable, restful environment. The room includes a panoramic lunar viewport, providing stunning views of the Moon’s surface and beyond. Ample storage space is built in to accommodate personal belongings and gear. Integrated within the bedroom is a small but efficient work area, designed for lunar-based projects or remote work. Equipped with ergonomic seating, a fold-out desk, and Earth-lunar communications capabilities, this workspace offers a peaceful, focused environment for productivity.\nOPEN-PLAN KITCHEN AND LIVING ROOM:\nA central, open space designed for communal living. The kitchen is equipped with advanced hydroponic food systems, enabling sustainable food production, and energy-efficient appliances designed for zero-gravity cooking. The living area provides a relaxing space with modular, multi-functional furniture that adapts to various configurations for lounging or socializing with guests.\nRECYCLING FACILITIES:\nEach unit includes individual, on-site recycling systems, specifically engineered for lunar waste management. The recycling facilities convert organic waste into usable resources, including oxygen and water, through advanced regenerative life-support technologies. Separate waste collection modules for non-organic materials are integrated into the unit for resource recovery.\nADDITIONAL AMENITIES:\nLIFE SUPPORT SYSTEMS:\nA robust life support system provides continuous air filtration, water purification, and temperature control, ensuring a safe and comfortable environment.\nCONNECTIVITY:\nThe unit is equipped with high-bandwidth communication arrays for Earth-lunar data exchange, facilitating constant connectivity for both personal and research needs.\n2. TERM OF LEASE\nThe term of this Agreement shall commence on 5/1/24 and shall remain in effect until 4/30/27, unless terminated earlier in accordance with this Agreement. The lease is renewable based on mutual agreement and availability of the lunar property.\n3. RENT\nThe Lessee agrees to pay the Lessor an amount of $3,125.00 per Month for the use of the property. Payments are due on the first of each lunar month and are to be made electronically to the Lessor\'s designated account on Earth.\n4. USE OF THE PROPERTY\nThe habitat units are exclusively designated for private living and remote work in a quiet and focused environment. These units are designed to support daily life and work activities for lunar residents, ensuring comfort and sustainability.\nThe use of the habitats for commercial purposes, public entertainment, parties, or similar social gatherings is strictly prohibited.\n5. COMPLIANCE WITH OUTER SPACE TREATY AND INTERNATIONAL LAWS\nBoth the Lessor and Lessee agree to comply with the provisions of the 1967 Outer Space Treaty and any other applicable international laws. Ownership of the lunar property is not recognized, but the lease grants the Lessee non-exclusive rights for exploration and use during the term of this Agreement.\n6. RESPONSIBILITIES AND MAINTENANCE\nThe Lessee shall be responsible for maintaining the habitability of the lunar habitat and all other leased facilities. Any damages caused by misuse or negligence will be the responsibility of the Lessee.\nThe Lessor shall ensure that the property is habitable at the start of the lease, including functional life support systems, solar energy generators, and communication devices.\n7. INSURANCE AND LIABILITY\nDue to the unique nature of space property, the Lessee agrees to obtain lunar insurance, covering both third-party liability and property damage, including damages resulting from space debris, meteor strikes, or unforeseen lunar surface incidents.\n8. TERMINATION\nEither party may terminate this Agreement with a 60-day written notice. The Lessor reserves the right to terminate the lease if the Lessee fails to comply with the terms, including payment, maintenance, or violation of international space law.\n9. GOVERNING LAW\nThis Agreement shall be governed by the principles outlined in the Outer Space Treaty, United Nations Space Law, and any applicable space regulations in place at the time.\n10. DISPUTE RESOLUTION\nIn the event of any disputes arising from this Agreement, both parties agree to submit to arbitration conducted by the United Nations Office for Outer Space Affairs (UNOOSA).\n11. MISCELLANEOUS\nTransfer of Lease: The Lessee shall not transfer or sublet the property without prior written consent from the Lessor.\nForce Majeure: Neither party shall be held responsible for delays or failures in performance due to circumstances beyond their control, including but not limited to space storms, mechanical failures, or launch delays.\n\n\nSIGNATURES\n\nLESSOR:\n\n\n________________________________________\nName: Schiaparelli plaza\nDate: 4/24/24\n\n\nLESSEE:\n\n\n________________________________________\nName: Marie Tharp\nDate: 4/24/24\n\n\n'}

    assert "SCHIAPARELLI PLAZA PROPERTY LEASE AGREEMENT" in docx_representation.get(
        "content", ""
    )
    assert "Lessor: Schiaparelli plaza" in docx_representation.get("content", "")

    assert img_file_id != "", "No .img file found in test files"

    docx_representation = box_file_text_extract(
        client=box_client_ccg, file_id=img_file_id
    )

    # Expected text in the img file
    # {'error': 'extracted_text representation is impossible for this file.', 'status': 'impossible'}

    assert (
        "impossible" in docx_representation.get("error", "").lower()
        or "error" in docx_representation.get("status", "").lower()
    )

    assert test_docx_file_id != "", "No .docx file found in test files"
    docx_representation = box_file_text_extract(
        client=box_client_ccg, file_id=test_docx_file_id
    )

    # Expected text in the docx file
    # {'content': 'AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation\n\nQingyun Wu , Gagan Bansal , Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Awadallah, Ryen W. White, Doug Burger, Chi Wang\n\n# Abstract\n\nAutoGen is an open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks. AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools. Using AutoGen, developers can also flexibly define agent interaction behaviors. Both natural language and computer code can be used to program flexible conversation patterns for different applications. AutoGen serves as a generic framework for building diverse applications of various complexities and LLM capacities. Empirical studies demonstrate the effectiveness of the framework in many example applications, with domains ranging from mathematics, coding, question answering, operations research, online decision-making, entertainment, etc.\n\n# Introduction\n\nLarge language models (LLMs) are becoming a crucial building block in developing powerful agents that utilize LLMs for reasoning, tool usage, and adapting to new observations (Yao et al., 2022; Xi et al., 2023; Wang et al., 2023b) in many real-world tasks. Given the expanding tasks that could benefit from LLMs and the growing task complexity, an intuitive approach to scale up the power of agents is to use multiple agents that cooperate. Prior work suggests that multiple agents can help encourage divergent thinking (Liang et al., 2023), improve factuality and reasoning (Du et al., 2023), and provide validation (Wu et al., 2023).\n\n## d666f1f7-46cb-42bd-9a39-9a39cf2a509f\n\nIn light of the intuition and early evidence of promise, it is intriguing to ask the following question: how can we facilitate the development of LLM applications that could span a broad spectrum of domains and complexities based on the multi-agent approach? Our insight is to use multi-agent conversations to achieve it. There are at least three reasons confirming its general feasibility and utility thanks to recent advances in LLMs: First, because chat optimized LLMs (e.g., GPT-4) show the ability to incorporate feedback, LLM agents can cooperate through conversations with each other or human(s), e.g., a dialog where agents provide and seek reasoning, observations, critiques, and validation. Second, because a single LLM can exhibit a broad range of capabilities (especially when configured with the correct prompt and inference settings), conversations between differently configured agents can help combine these broad LLM capabilities in a modular and complementary manner. Third, LLMs have demonstrated ability to solve complex tasks when the tasks are broken into simpler subtasks. Here is a random UUID in the middle of the paragraph! 314b0a30-5b04-470b-b9f7-eed2c2bec74a Multi-agent conversations can enable this partitioning and integration in an intuitive manner. How can we leverage the above insights and support different applications with the common requirement of coordinating multiple agents, potentially backed by LLMs, humans, or tools exhibiting different capacities? We desire a multi-agent conversation framework with generic abstraction and effective implementation that has the flexibility to satisfy different application needs. Achieving this requires addressing two critical questions: (1) How can we design individual agents that are capable, reusable, customizable, and effective in multi-agent collaboration? (2) How can we develop a straightforward, unified interface that can accommodate a wide range of agent conversation patterns? In practice, applications of varying complexities may need distinct sets of agents with specific capabilities, and may require different conversation patterns, such as single- or multi-turn dialogs, different human involvement modes, and static vs. dynamic conversation. Moreover, developers may prefer the flexibility to program agent interactions in natural language or code. Failing to adequately address these two questions would limit the framework’s scope of applicability and generality.\n\nHere is a random table for .docx parsing test purposes:\n\n|  |  |  |  |  |  |\n| --- | --- | --- | --- | --- | --- |\n| 1 | 2 | 3 | 4 | 5 | 6 |\n| 7 | 8 | 9 | 10 | 11 | 12 |\n| 13 | 14 | 49e168b7-d2ae-407f-a055-2167576f39a1 | 15 | 16 | 17 |\n| 18 | 19 | 20 | 21 | 22 | 23 |\n| 24 | 25 | 26 | 27 | 28 | 29 |\n\nTest Image:\n\n![图形用户界面, 文本, 应用程序, 信件  AI 生成的内容可能不正确。](data:image/png;base64...)'}
    assert (
        "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent"
        in docx_representation.get("content", "")
    )
