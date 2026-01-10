"""
Financial Accelerator Classification Interface
===============================================
Streamlit application for human validation of Claude's classifications
of FOMC speaker beliefs about the financial accelerator/credit channel -
how credit market conditions amplify economic shocks through feedback effects.

Following Mullainathan et al. (2024) framework for LLM output validation.

Usage:
    streamlit run coding_interface.py
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import io


def get_script_directory():
    """Get the directory where this script is located."""
    return Path(__file__).resolve().parent


SCRIPT_DIR = get_script_directory()

# Columns that are hidden from coders during classification
HIDDEN_COLUMNS = ['claude_credit_channel', 'claude_credit_channel_category']

# Columns included in output (alongside human coding)
OUTPUT_COLUMNS = [
    'coding_id', 'original_index', 'coder_name', 'classification',
    'claude_credit_channel', 'claude_credit_channel_category',
    'quotation', 'description', 'variable', 'stablespeaker', 'ymd',
    'notes', 'coded_at'
]

# Page configuration
st.set_page_config(
    page_title="Financial Accelerator Classification",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_coding_data_from_file(file_content):
    """Load the coding sample data from uploaded file."""
    return pd.read_csv(io.StringIO(file_content.decode('utf-8')))


@st.cache_data
def load_default_coding_data():
    """Load the default coding data from the repo."""
    coding_file = SCRIPT_DIR / 'validation_samples' / 'production' / 'coding_financial_accelerator.csv'
    if coding_file.exists():
        return pd.read_csv(coding_file)
    return None


def get_results_csv(results, coding_df):
    """
    Convert results to CSV for download.
    Includes Claude's classifications and key columns from the source data.
    """
    results_df = pd.DataFrame(results)

    # Merge with coding_df to get all the extra columns
    merged = results_df.merge(
        coding_df[['coding_id', 'original_index', 'quotation', 'description',
                   'variable', 'stablespeaker', 'ymd',
                   'claude_credit_channel', 'claude_credit_channel_category']],
        on='coding_id',
        how='left'
    )

    # Reorder columns for clarity
    output_cols = [c for c in OUTPUT_COLUMNS if c in merged.columns]
    merged = merged[output_cols]

    return merged.to_csv(index=False).encode('utf-8')


def get_previous_coding(coding_id, results):
    """Get previous coding values for a specific coding_id."""
    for result in results:
        if result.get('coding_id') == coding_id:
            return result
    return None


def validate_resume_csv(resume_df, coding_df):
    """
    Validate that a resume CSV is compatible with the current coding data.

    Returns:
        tuple: (is_valid, message, matching_ids)
    """
    required_cols = {'coding_id', 'coder_name', 'classification'}
    if not required_cols.issubset(resume_df.columns):
        missing = required_cols - set(resume_df.columns)
        return False, f"Missing required columns: {missing}", set()

    resume_ids = set(resume_df['coding_id'].tolist())
    coding_ids = set(coding_df['coding_id'].tolist())

    matching_ids = resume_ids.intersection(coding_ids)
    unmatched_ids = resume_ids - coding_ids

    if len(matching_ids) == 0:
        return False, "No coding_ids in resume file match current data source", set()

    if len(unmatched_ids) > 0:
        return True, f"Warning: {len(unmatched_ids)} coding_ids in resume file not found in current data (will be ignored)", matching_ids

    return True, f"Successfully validated {len(matching_ids)} coded arguments", matching_ids


def initialize_session_state():
    """Initialize all session state variables."""
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'coded_ids' not in st.session_state:
        st.session_state.coded_ids = set()
    if 'widget_version' not in st.session_state:
        st.session_state.widget_version = 0
    if 'locked_coder_name' not in st.session_state:
        st.session_state.locked_coder_name = None


def main():
    st.title("Financial Accelerator Classification")
    st.markdown("**Human Validation of LLM Classifications**")
    st.markdown("---")

    # Initialize session state
    initialize_session_state()

    # Sidebar setup
    with st.sidebar:
        st.header("Setup")

        # Coder identification
        if st.session_state.locked_coder_name is not None:
            st.text_input(
                "Your Name (locked)",
                value=st.session_state.locked_coder_name,
                disabled=True,
                help="Name is locked after first save to ensure consistency"
            )
            coder_name = st.session_state.locked_coder_name
        else:
            coder_name = st.text_input(
                "Your Name",
                placeholder="Enter your name",
                help="Used to identify your coding results. Will be locked after first save."
            )

        if not coder_name:
            st.warning("Please enter your name to begin")
            st.stop()

        # Data source selection
        st.markdown("---")
        st.subheader("Data Source")

        data_source = st.radio(
            "Choose data source:",
            ["Use default sample", "Upload custom file"],
            help="Use the pre-loaded sample or upload your own CSV"
        )

        coding_df = None

        if data_source == "Use default sample":
            coding_df = load_default_coding_data()
            if coding_df is None:
                st.error("Default coding file not found. Please upload a file.")
                st.stop()
            else:
                st.success(f"Loaded {len(coding_df)} arguments")
        else:
            uploaded_file = st.file_uploader(
                "Upload Coding File",
                type=['csv'],
                help="Upload a coding CSV file"
            )
            if uploaded_file:
                coding_df = load_coding_data_from_file(uploaded_file.getvalue())
                st.success(f"Loaded {len(coding_df)} arguments")
            else:
                st.info("Please upload a coding file")
                st.stop()

    total_arguments = len(coding_df)
    current_index = st.session_state.current_index

    # Get current widget version for keying
    v = st.session_state.widget_version

    # Progress tracking in sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("Progress")

        n_coded = len(st.session_state.coded_ids)
        progress_pct = n_coded / total_arguments if total_arguments > 0 else 0
        st.progress(progress_pct)
        st.write(f"Coded: {n_coded} / {total_arguments}")
        st.write(f"Current: Argument {current_index + 1}")

        # Download results button
        st.markdown("---")
        st.subheader("Save Results")

        if st.session_state.results:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = coder_name.lower().replace(' ', '_')
            filename = f"coded_{safe_name}_financial_accelerator_{timestamp}.csv"

            st.download_button(
                label="Download Results CSV",
                data=get_results_csv(st.session_state.results, coding_df),
                file_name=filename,
                mime="text/csv",
                help="Download your coding results (includes Claude's classifications)"
            )
            st.caption(f"{len(st.session_state.results)} arguments coded")
        else:
            st.info("Code some arguments to enable download")

        # Load previous session via upload
        st.markdown("---")
        st.subheader("Resume Session")

        resume_file = st.file_uploader(
            "Upload previous session",
            type=['csv'],
            key="resume_upload",
            help="Upload a previously downloaded results file to continue"
        )

        if resume_file:
            if st.button("Load Session"):
                try:
                    resume_df = pd.read_csv(resume_file)

                    # Validate the resume CSV
                    is_valid, message, matching_ids = validate_resume_csv(resume_df, coding_df)

                    if not is_valid:
                        st.error(f"Cannot load session: {message}")
                    else:
                        if "Warning" in message:
                            st.warning(message)

                        # Filter to only matching IDs and extract just the coding results
                        valid_resume = resume_df[resume_df['coding_id'].isin(matching_ids)]
                        valid_results = []
                        for _, row in valid_resume.iterrows():
                            valid_results.append({
                                'coding_id': row['coding_id'],
                                'coder_name': row['coder_name'],
                                'classification': row['classification'],
                                'notes': row.get('notes', ''),
                                'coded_at': row.get('coded_at', datetime.now().isoformat())
                            })

                        st.session_state.results = valid_results
                        st.session_state.coded_ids = set(r['coding_id'] for r in valid_results)

                        # Lock the coder name from the resume file
                        if len(valid_results) > 0:
                            st.session_state.locked_coder_name = valid_results[0].get('coder_name', coder_name)

                        # INCREMENT WIDGET VERSION to force fresh widget state
                        st.session_state.widget_version += 1

                        # Jump to first uncoded argument
                        found_uncoded = False
                        for idx in range(len(coding_df)):
                            if coding_df.iloc[idx]['coding_id'] not in st.session_state.coded_ids:
                                st.session_state.current_index = idx
                                found_uncoded = True
                                break

                        if not found_uncoded:
                            st.session_state.current_index = len(coding_df) - 1

                        st.success(f"Loaded {len(valid_results)} coded arguments")
                        st.rerun()

                except Exception as e:
                    st.error(f"Error loading session: {e}")

    # Main coding area
    if current_index < total_arguments:
        current_row = coding_df.iloc[current_index]
        coding_id = current_row['coding_id']
        quotation = current_row['quotation']
        description = current_row.get('description', '')
        explanation = current_row.get('explanation', '')
        variable = current_row.get('variable', '')

        is_coded = coding_id in st.session_state.coded_ids
        previous_coding = get_previous_coding(coding_id, st.session_state.results) if is_coded else None

        # Two-column layout
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader(f"Argument {coding_id}")

            if variable:
                st.caption(f"Economic Variable: **{variable}**")

            if is_coded:
                st.success("Already coded - you can update or skip")

            # Quotation
            st.markdown("**Quotation:**")
            st.markdown(
                f"""<div style="background-color: #f0f2f6; padding: 20px;
                border-radius: 10px; font-size: 16px; line-height: 1.6;">
                {quotation}
                </div>""",
                unsafe_allow_html=True
            )

            # Description
            if pd.notna(description) and str(description).strip():
                st.markdown("**Description:**")
                st.markdown(
                    f"""<div style="background-color: #e8f4f8; padding: 15px;
                    border-radius: 8px; font-size: 14px; margin-top: 10px;">
                    {description}
                    </div>""",
                    unsafe_allow_html=True
                )

            # Explanation
            if pd.notna(explanation) and str(explanation).strip():
                st.markdown("**Explanation:**")
                st.markdown(
                    f"""<div style="background-color: #fff4e6; padding: 15px;
                    border-radius: 8px; font-size: 14px; margin-top: 10px;">
                    {explanation}
                    </div>""",
                    unsafe_allow_html=True
                )

        with col2:
            st.subheader("Classification")

            st.markdown("""
            **Does this speaker express a belief about the financial accelerator
            or credit channel?**

            *(Whether credit market conditions AMPLIFY economic shocks through
            feedback effects between financial conditions and real activity)*
            """)

            # Get default value from previous coding
            categories = ['strong', 'weak', 'moderate', 'none']
            category_labels = {
                'strong': 'STRONG - Credit markets SIGNIFICANTLY amplify economic shocks',
                'weak': 'WEAK - Credit markets have LITTLE/NO amplifying effect',
                'moderate': 'MODERATE - Qualified/partial amplification',
                'none': 'NONE - No financial accelerator belief expressed'
            }

            default_idx = 3  # Default to none
            if previous_coding:
                prev_cat = previous_coding.get('classification', 'none')
                if prev_cat in categories:
                    default_idx = categories.index(prev_cat)

            classification = st.radio(
                "Select classification:",
                options=categories,
                format_func=lambda x: category_labels[x],
                index=default_idx,
                key=f"classification_{current_index}_v{v}"
            )

            # Optional notes
            st.markdown("---")
            notes_default = ''
            if previous_coding:
                notes_val = previous_coding.get('notes', '')
                if isinstance(notes_val, str) and pd.notna(notes_val):
                    notes_default = notes_val

            notes = st.text_area(
                "Notes (optional):",
                value=notes_default,
                max_chars=500,
                key=f"notes_{current_index}_v{v}",
                help="Any observations or issues with this argument"
            )

            # Classification guide
            with st.expander("Classification Guide"):
                st.markdown("""
                ## What is the Financial Accelerator?

                The financial accelerator describes how shocks to the economy are
                **amplified through feedback effects** between credit market conditions
                and real economic activity. Key concept: **amplification/feedback**,
                not just direct effects.

                ---

                ### STRONG

                The speaker indicates credit market conditions **SIGNIFICANTLY AMPLIFY**
                economic shocks through feedback mechanisms.

                **Key indicators:**
                - Amplification language: "magnifies", "amplifies", "multiplies", "reinforces"
                - Feedback/spiral language: "feedback loop", "self-reinforcing", "spiral", "cascade"
                - Causal chains: "tighter credit -> weaker balance sheets -> tighter credit"
                - Concern about propagation: "spillover", "contagion", "transmission"

                **Examples:**
                - "Tighter credit conditions are amplifying the downturn as weakening
                  balance sheets further constrain lending"
                - "We're seeing a self-reinforcing cycle where credit constraints
                  reduce spending, which weakens balance sheets, which tightens credit"
                - "Balance sheet effects are creating powerful feedback mechanisms"

                ---

                ### WEAK

                The speaker indicates credit markets have **LITTLE or NO amplifying effect**
                on economic shocks.

                **Key indicators:**
                - Disconnection: "despite tight credit", "credit hasn't constrained"
                - Direct only: "one-time effect", "no feedback"
                - Resilience: "strong balance sheets", "well-capitalized"
                - Other factors: "driven by fundamentals not credit"

                **Examples:**
                - "Despite tighter lending standards, business investment has remained robust"
                - "The credit channel appears quite weak in this cycle"
                - "Credit conditions affect activity, but we're not seeing multiplier effects"

                ---

                ### MODERATE

                The speaker indicates a **QUALIFIED or PARTIAL** amplification mechanism.

                **Key indicators:**
                - Hedging: "some amplification", "modest feedback", "limited reinforcement"
                - Conditionality: "depends on balance sheet strength", "varies by sector"
                - Weakening: "less amplification than past cycles"

                **Examples:**
                - "Credit conditions are creating some amplification, but effects are
                  more modest than in previous cycles"
                - "Small businesses face credit constraints that amplify shocks,
                  though large firms have ample access"

                ---

                ### NONE (default)

                **No financial accelerator belief expressed.**

                Use NONE when:
                - Only mentions credit OR real activity (not both)
                - Mentions both but no causal/amplification connection
                - Describes data without interpreting amplification mechanism
                - Discusses policy without explaining credit channel transmission
                - Describes one-time/direct effects without feedback dynamics

                **Key distinction:** Simple "credit affects spending" is NOT enough.
                Must show AMPLIFICATION, FEEDBACK, or REINFORCING dynamics.

                ---

                ### Special Cases

                **Forecasts:** Only classify if reasoning reveals credit channel logic
                - "I forecast slower growth" -> NONE
                - "I forecast slower growth because credit tightening will amplify" -> STRONG

                **Historical references:** Only classify if speaker endorses/rejects mechanism
                - "Credit was tight in 2008" -> NONE
                - "2008 showed how credit dynamics amplify shocks" -> STRONG

                **One-time vs. Feedback:**
                - "Higher rates will reduce credit-financed spending" -> NONE (direct)
                - "Higher rates will trigger feedback where falling collateral
                  values tighten credit further" -> STRONG (amplification)

                ---

                *When in doubt, select NONE.*
                """)

        # Navigation
        st.markdown("---")
        col_prev, col_save, col_next, col_jump = st.columns([1, 2, 1, 2])

        with col_prev:
            if st.button("Previous", disabled=(current_index == 0), use_container_width=True):
                st.session_state.current_index -= 1
                st.rerun()

        with col_save:
            if st.button("Save & Continue", type="primary", use_container_width=True):
                # Lock coder name on first save
                if st.session_state.locked_coder_name is None:
                    st.session_state.locked_coder_name = coder_name

                result = {
                    'coding_id': coding_id,
                    'coder_name': st.session_state.locked_coder_name,
                    'classification': classification,
                    'notes': notes,
                    'coded_at': datetime.now().isoformat()
                }

                # Update or append
                existing_idx = None
                for i, r in enumerate(st.session_state.results):
                    if r['coding_id'] == coding_id:
                        existing_idx = i
                        break

                if existing_idx is not None:
                    st.session_state.results[existing_idx] = result
                else:
                    st.session_state.results.append(result)

                st.session_state.coded_ids.add(coding_id)

                st.success(f"Saved! ({len(st.session_state.results)} total)")

                # Move to next
                if current_index < total_arguments - 1:
                    st.session_state.current_index += 1
                    st.rerun()

        with col_next:
            if st.button("Skip", disabled=(current_index == total_arguments - 1), use_container_width=True):
                st.session_state.current_index += 1
                st.rerun()

        with col_jump:
            jump_to = st.number_input(
                "Jump to:",
                min_value=1,
                max_value=total_arguments,
                value=current_index + 1,
                step=1,
                key=f"jump_{current_index}_v{v}"
            )
            if st.button("Go", use_container_width=True):
                st.session_state.current_index = jump_to - 1
                st.rerun()

    else:
        st.success("All arguments have been reviewed!")
        st.info(f"Total coded: {len(st.session_state.coded_ids)} / {total_arguments}")

        st.markdown("### Download your results:")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = coder_name.lower().replace(' ', '_')
        filename = f"coded_{safe_name}_financial_accelerator_{timestamp}.csv"

        st.download_button(
            label="Download Results CSV",
            data=get_results_csv(st.session_state.results, coding_df),
            file_name=filename,
            mime="text/csv",
            type="primary"
        )

        if st.button("Return to Start"):
            st.session_state.current_index = 0
            st.rerun()


if __name__ == "__main__":
    main()
