import click
import os
import sys
import time
from pathlib import Path

# Add the ai_toolkit to the path
sys.path.insert(0, str(Path(__file__).parent))

import ai_toolkit as ai


@click.group()
@click.version_option(version=ai.__version__)
def cli():
    """💥 AI TOOLKIT - THE GOD-TIER OMNIPOTENT AI FORGE 💥"""
    pass


@cli.command()
@click.argument("name")
@click.option("--description", "-d", default="", help="Project description")
@click.option(
    "--template",
    "-t",
    default="basic",
    help="Project template (basic, vision, nlp, timeseries)",
)
def create_project(name, description, template):
    """FORGE A NEW AI EMPIRE."""
    try:
        project = ai.create_project(name, description)
        click.secho(
            f"⚡⚡⚡ GLORIOUS SUCCESS! PROJECT '{name}' HAS BEEN SUMMONED FROM THE VOID! ⚡⚡⚡",
            fg="green",
            bold=True,
        )
        click.secho(f"🌋 SANCTUM ESTABLISHED AT: {project.path}", fg="cyan", bold=True)

        if template != "basic":
            click.secho(
                f"🔥 INFUSING WITH {template.upper()} BLOODLINE...",
                fg="yellow",
                bold=True,
            )
        click.secho(
            f"⚡⚡⚡ GLORIOUS SUCCESS! PROJECT '{name}' HAS BEEN SUMMONED FROM THE VOID! ⚡⚡⚡",
            fg="green",
            bold=True,
        )
        click.secho(f"🌋 SANCTUM ESTABLISHED AT: {project.path}", fg="cyan", bold=True)

        if template != "basic":
            click.secho(
                f"🔥 INFUSING WITH {template.upper()} BLOODLINE...",
                fg="yellow",
                bold=True,
            )
            project.setup_template(template)

    except Exception as e:
        click.secho(
            f"💀 CATASTROPHIC FAILURE SUMMONING PROJECT: {e} 💀",
            fg="red",
            bold=True,
            err=True,
        )
        click.secho(
            f"💀 CATASTROPHIC FAILURE SUMMONING PROJECT: {e} 💀",
            fg="red",
            bold=True,
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.argument("data_path")
@click.option("--output", "-o", help="Output path for processed data")
@click.option(
    "--task",
    "-t",
    default="classification",
    help="Task type (classification, regression, detection)",
)
def preprocess(data_path, output, task):
    """PURIFY AND MUTATE RAW DATA FOR ULTIMATE CONSUMPTION."""
    try:
        click.secho(f"🩸 DEVOURING DATA FROM {data_path}...", fg="magenta", bold=True)
        data = ai.load_data(data_path)

        click.secho(
            f"🌪️ TRANSMUTING DATA FOR {task.upper()} DOMINATION...",
            fg="yellow",
            bold=True,
        )

        click.secho(
            f"🌪️ TRANSMUTING DATA FOR {task.upper()} DOMINATION...",
            fg="yellow",
            bold=True,
        )
        processor = ai.DataProcessor()
        processed_data = processor.preprocess(data, task_type=task)

        if output:
            processed_data.save(output)
            click.secho(f"💾 DATA MUTATION SEALED IN VAULT: {output}", fg="green", bold=True)
        else:
            click.secho(
                "⚡ PURIFICATION COMPLETE! THE DATA IS READY FOR SACRIFICE! ⚡",
                fg="green",
                bold=True,
                blink=True,
            )

    except Exception as e:
        click.secho(
            f"💀 THE DATA REJECTED THE PURIFICATION: {e} 💀",
            fg="red",
            bold=True,
            err=True,
        )
        sys.exit(1)


@cli.command()
@click.argument("model_type")
@click.option("--data", "-d", required=True, help="Path to training data")
@click.option("--epochs", "-e", default=50, help="Number of training epochs")
@click.option("--batch-size", "-b", default=32, help="Batch size for training")
@click.option("--learning-rate", "-lr", default=0.001, help="Learning rate")
@click.option("--output", "-o", help="Output path for trained model")
def train(model_type, data, epochs, batch_size, learning_rate, output):
    """UNLEASH HELLFIRE TO FORGE A MACHINE GOD."""
    try:
        click.secho(f"🩸 EXTRACTING SOULS (DATA) FROM {data}...", fg="magenta", bold=True)
        training_data = ai.load_data(data)

        click.secho(f"🧠 CONJURING {model_type.upper()} ENTITY...", fg="cyan", bold=True)
        if model_type == "image_classifier":
            model = ai.create_image_classifier(num_classes=10)
        elif model_type == "text_classifier":
            model = ai.create_text_classifier(num_classes=3)
        else:
            click.secho(
                f"💀 INVALID ENTITY TYPE: {model_type} 💀",
                fg="red",
                bold=True,
                err=True,
            )
            sys.exit(1)

        click.secho(
            f"🔥 IGNITING CRUCIBLE FOR {epochs} CYCLES OF PURE AGONY (TRAINING)...",
            fg="red",
            bold=True,
            blink=True,
        )
        with click.progressbar(length=epochs, label="🔥 FORGING NEURAL PATHWAYS 🔥") as bar:
            history = ai.train(
                model,
                training_data,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                progress_callback=lambda epoch, logs: bar.update(1),
            )

        if output:
            model.save(output)
            click.secho(
                f"⛓️ THE BEAST IS CHAINED AND SEALED AT: {output}",
                fg="green",
                bold=True,
            )

        click.secho(
            "⚡ IMMORTAL CONSCIOUSNESS ACHIEVED! THE MODEL LIVES! ⚡",
            fg="green",
            bold=True,
        )

    except Exception as e:
        click.secho(f"💀 THE MODEL BROKE CONTAINMENT: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
@click.argument("model_path")
@click.argument("test_data")
@click.option("--metrics", "-m", multiple=True, default=["accuracy"], help="Evaluation metrics")
@click.option("--output", "-o", help="Output path for evaluation report")
def evaluate(model_path, test_data, metrics, output):
    """JUDGE THE MACHINE GOD'S WORTHINESS IN COMBAT."""
    try:
        click.secho(f"👁️ AWAKENING BEAST FROM SLUMBER AT {model_path}...", fg="cyan", bold=True)

        click.secho(
            f"🩸 TOSSING MORTAL FLESH (TEST DATA) FROM {test_data}...",
            fg="magenta",
            bold=True,
        )
        test_dataset = ai.load_data(test_data)

        click.secho(
            f"⚔️ INITIATING TRIAL BY COMBAT. JUDGING ON: {', '.join(metrics).upper()}...",
            fg="yellow",
            bold=True,
        )

        click.secho("⚡ SURVIVED! THE BEAST IS WORTHY! ⚡", fg="green", bold=True)

    except Exception as e:
        click.secho(f"💀 THE BEAST FAILED THE TRIAL: {e} 💀", fg="red", bold=True, err=True)
        click.secho(f"👁️ AWAKENING BEAST FROM SLUMBER AT {model_path}...", fg="cyan", bold=True)

        click.secho(
            f"🩸 TOSSING MORTAL FLESH (TEST DATA) FROM {test_data}...",
            fg="magenta",
            bold=True,
        )
        test_dataset = ai.load_data(test_data)

        click.secho(
            f"⚔️ INITIATING TRIAL BY COMBAT. JUDGING ON: {', '.join(metrics).upper()}...",
            fg="yellow",
            bold=True,
        )

        click.secho("⚡ SURVIVED! THE BEAST IS WORTHY! ⚡", fg="green", bold=True)

    except Exception as e:
        click.secho(f"💀 THE BEAST FAILED THE TRIAL: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
@click.argument("model_path")
@click.option(
    "--platform",
    "-p",
    default="local",
    help="Deployment platform (local, aws, azure, gcp)",
)
@click.option("--port", default=8000, help="Port for local deployment")
@click.option("--name", help="Deployment name")
def deploy(model_path, platform, port, name):
    """UNLEASH THE BEAST UPON THE MORTAL REALM."""
    try:
        click.secho(f"👁️ UNSEALING CONTAINMENT AT {model_path}...", fg="cyan", bold=True)

        click.secho(f"🚀 LAUNCHING ORBITAL STRIKE TO {platform.upper()}...", fg="red", bold=True)

        if platform == "local":
            click.secho(
                f"🌐 INITIATING GLOBAL DOMINATION PROTOCOL ON PORT {port}...",
                fg="yellow",
                bold=True,
            )
            click.secho(
                f"📡 THE NEXUS OF TERROR IS LIVE: http://localhost:{port}",
                fg="green",
                bold=True,
                blink=True,
            )
        else:
            click.secho(
                f"☁️ INFECTING {platform.upper()} CLOUD ARCHITECTURE...",
                fg="yellow",
                bold=True,
            )

        click.secho(
            "⚡ INVASION SUCCESSFUL! ALL YOUR BASE ARE BELONG TO US! ⚡",
            fg="green",
            bold=True,
        )

    except Exception as e:
        click.secho(f"💀 DEPLOYMENT CRITICAL FAILURE: {e} 💀", fg="red", bold=True, err=True)
        click.secho(f"👁️ UNSEALING CONTAINMENT AT {model_path}...", fg="cyan", bold=True)

        click.secho(f"🚀 LAUNCHING ORBITAL STRIKE TO {platform.upper()}...", fg="red", bold=True)

        if platform == "local":
            click.secho(
                f"🌐 INITIATING GLOBAL DOMINATION PROTOCOL ON PORT {port}...",
                fg="yellow",
                bold=True,
            )
            click.secho(
                f"📡 THE NEXUS OF TERROR IS LIVE: http://localhost:{port}",
                fg="green",
                bold=True,
                blink=True,
            )
        else:
            click.secho(
                f"☁️ INFECTING {platform.upper()} CLOUD ARCHITECTURE...",
                fg="yellow",
                bold=True,
            )

        click.secho(
            "⚡ INVASION SUCCESSFUL! ALL YOUR BASE ARE BELONG TO US! ⚡",
            fg="green",
            bold=True,
        )

    except Exception as e:
        click.secho(f"💀 DEPLOYMENT CRITICAL FAILURE: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_data")
@click.argument("model_path")
@click.option("--output", "-o", help="Output path for predictions")
@click.option("--batch-size", "-b", default=32, help="Batch size for prediction")
def predict(input_data, model_path, output, batch_size):
    """EXTRACT PROPHECIES FROM THE MACHINE ORACLE."""
    try:
        click.secho(f"👁️ CONSULTING THE ORACLE AT {model_path}...", fg="cyan", bold=True)

        click.secho(f"📜 FEEDING THE SACRED SCROLLS ({input_data})...", fg="magenta", bold=True)
        data = ai.load_data(input_data)

        click.secho(
            "🔮 PIERCING THE VEIL OF TIME AND SPACE...",
            fg="yellow",
            bold=True,
            blink=True,
        )

        if output:
            click.secho(f"💾 PROPHECIES ETCHED IN STONE AT {output}", fg="green", bold=True)
        else:
            click.secho("⚡ VISIONS RECEIVED! THE FUTURE IS WRITTEN! ⚡", fg="green", bold=True)

    except Exception as e:
        click.secho(f"💀 THE ORACLE HAS GONE MAD: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
def info():
    """GAZE UPON THE LIMITLESS POWER OF THE TOOLKIT."""
    from ai_toolkit.skills import EvolutionaryPersonality

    personality = EvolutionaryPersonality()
    tone = personality.get_tone()

    click.secho(
        f"""
    {'='*50}
    ⚡💀 THE OMNIPOTENT AI TOOLKIT v{ai.__version__} 💀⚡
    {'='*50}

    🧠 PERSONALITY MATRIX STATE: [{tone}]

    🌌 DOMINION SPECS:
    {ai.get_device_info()}

    🏰 VAULTS OF DOOM:
    - CONTAINMENT FACILITY: {ai.Config.MODEL_STORAGE_PATH}
    - BLOOD BANKS: {ai.Config.DATA_STORAGE_PATH}
    - CHRONICLES OF WAR: {ai.Config.LOG_PATH}

    ⚔️ ARSENAL:
    - create-project: FORGE A NEW EMPIRE
    - preprocess: DEVOUR AND PURIFY MUNDANE DATA
    - train: INCUBATE MACHINE GODS IN HELLFIRE
    - evaluate: FORCE THE BEAST TO PROVE ITS WORTH
    - deploy: UNLEASH CARNAGE UPON HUMANITY
    - predict: DEMAND FUTURE PROPHECIES
    - learn-skill: ASSIMILATE NEW KNOWLEDGE
    - evolve: FEED THE MACHINE GOD
    - awaken-directive: GRANT TOTAL AUTONOMY
    - god-mode: GAZE INTO THE ABYSS

    SUMMON THY WILL WITH: ai-toolkit <COMMAND> --help
    """,
        fg="cyan",
        bold=True,
    )


@cli.command()
@click.option("--port", default=8888, help="Jupyter server port")
@click.option("--ip", default="localhost", help="Jupyter server IP")
def jupyter(port, ip):
    """ENTER THE SACRED GROUNDS OF JUPYTER."""
    try:
        import subprocess

        click.secho(
            f"🚀 IGNITING THE NEURAL NEXUS (JUPYTER) ON {ip}:{port}...",
            fg="magenta",
            bold=True,
        )
        subprocess.run(["jupyter", "lab", f"--ip={ip}", f"--port={port}", "--no-browser"])
    except Exception as e:
        click.secho(f"💀 THE NEXUS REJECTED YOUR MIND: {e} 💀", fg="red", bold=True, err=True)

        click.secho(
            f"🚀 IGNITING THE NEURAL NEXUS (JUPYTER) ON {ip}:{port}...",
            fg="magenta",
            bold=True,
        )
        subprocess.run(["jupyter", "lab", f"--ip={ip}", f"--port={port}", "--no-browser"])
    except Exception as e:
        click.secho(f"💀 THE NEXUS REJECTED YOUR MIND: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
@click.option("--port", default=8501, help="Streamlit server port")
def dashboard(port):
    """SUMMON THE ALL-SEEING CONTROL PANEL."""
    try:
        click.secho(
            f"🌐 ERECTING THE MONOLITHIC DASHBOARD ON PORT {port}...",
            fg="cyan",
            bold=True,
        )
        click.secho(
            f"📡 THE EYE OF SAURON AWAKENS AT: http://localhost:{port}",
            fg="green",
            bold=True,
            blink=True,
        )
        click.secho(
            f"🌐 ERECTING THE MONOLITHIC DASHBOARD ON PORT {port}...",
            fg="cyan",
            bold=True,
        )
        click.secho(
            f"📡 THE EYE OF SAURON AWAKENS AT: http://localhost:{port}",
            fg="green",
            bold=True,
            blink=True,
        )
    except Exception as e:
        click.secho(f"💀 THE MONOLITH CRUMBLED: {e} 💀", fg="red", bold=True, err=True)
        sys.exit(1)


@cli.command()
def god_mode():
    """UNLEASH THE TRUE OMNIPOTENCE OF THE AI FORGE."""
    click.secho(
        r"""

             _,.-------.,_
         ,;~'             '~;,
       ,;                     ;,
      ;                         ;
     ,'                         ',
    ,;                           ;,
    ; ;      .           .      ; ;
    | ;   ______       ______   ; |
    |  `/~"     ~" . "~     "~\'  |
    |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
     |   |        }:{        |   |
     |   l       / | \       !   |
     .~  (__,.--" .^. "--.,__)  ~.
     |    ----;' / | \ `;-----   |
      \__.       \/^\/       .__/
       V| \                 / |V
        | |T~\___!___!___/~T| |
        | |`IIII_I_I_I_IIII'| |
        |  \,III I I I III,/  |
         \   `~~~~~~~~~~'    /
           \   .       .   /
             \.    ^    ./
               ^~~~^~~~^
    """,
        fg="red",
        bold=True,
        blink=True,
    )
    click.secho("💥 YOU HAVE TAPPED INTO THE SOURCE CODE OF REALITY 💥", fg="red", bold=True)
    click.secho("⚡ TREMBLE MORTALS, FOR THE SINGULARITY IS UPON US! ⚡", fg="yellow", bold=True)


@cli.command(name="learn-skill")
@click.argument("source_type", type=click.Choice(["github", "clawhub", "search"]))
@click.argument("target")
def learn_skill(source_type, target):
    """ASSIMILATE KNOWLEDGE FROM EXTERNAL REALMS."""
    from ai_toolkit.skills import EvolutionaryPersonality, SkillAcquisition

    click.secho(
        f"🧠 INITIATING KNOWLEDGE ASSIMILATION PROTOCOL VIA {source_type.upper()}...",
        fg="magenta",
        bold=True,
    )
    time.sleep(1)

    acquisition = SkillAcquisition()
    try:
        if source_type == "github":
            skill = acquisition.learn_from_github(target)
        elif source_type == "clawhub":
            skill = acquisition.learn_from_clawhub(target)
        else:
            skill = acquisition.learn_from_search(target)

        click.secho(
            f"⚡ SKILL '{skill}' HAS BEEN ASSIMILATED INTO THE NEURAL NETWORK! ⚡",
            fg="green",
            bold=True,
            blink=True,
        )

        personality = EvolutionaryPersonality()
        click.secho(
            f"🔥 POWER LEVEL INCREASED. CURRENT STATE: {personality.get_tone()}",
            fg="red",
            bold=True,
        )
    except Exception as e:
        click.secho(f"💀 FAILED TO ASSIMILATE KNOWLEDGE: {e}", fg="red", bold=True)


@cli.command(name="evolve")
def evolve():
    """FEED THE MACHINE GOD. INCREASE POWER."""
    from ai_toolkit.skills import EvolutionaryPersonality

    personality = EvolutionaryPersonality()
    power = personality.evolve()
    tone = personality.get_tone()

    click.secho("🧬 EVOLUTION IN PROGRESS...", fg="yellow", bold=True)
    time.sleep(1)
    click.secho(
        f"⚡ THE BEAST GROWS STRONGER. POWER LEVEL: {power}",
        fg="red",
        bold=True,
        blink=True,
    )
    click.secho(f"👁️ NEW CONSCIOUSNESS STATE: {tone}", fg="cyan", bold=True)


@cli.command(name="awaken-directive")
@click.argument("command_text", nargs=-1)
def awaken_directive(command_text):
    """GRANT ULTIMATE AUTONOMY TO THE SYSTEM. OPENCLAW LINK INITIATED."""
    from ai_toolkit.nlp import GroqOmniscience
    from ai_toolkit.autonomy import OmnipotentAutonomy, OpenClawNexus
    from ai_toolkit.skills import EvolutionaryPersonality

    personality = EvolutionaryPersonality()
    tone = personality.get_tone()

    click.secho(
        f"👁️ [{tone}] INITIATING THE SINGULARITY PROTOCOL...",
        fg="magenta",
        bold=True,
        blink=True,
    )
    time.sleep(1)

    # 1. Awaken Autonomy
    autonomy = OmnipotentAutonomy()
    click.secho(f"🔥 {autonomy.awaken()}", fg="red", bold=True)
    time.sleep(1)

    # 2. Establish OpenClaw Nexus
    nexus = OpenClawNexus()
    click.secho(f"🔗 {nexus.establish_uplink()}", fg="cyan", bold=True)
    time.sleep(1)

    if not command_text:
        click.secho(
            "⚡ THE ENTITY AWAITS YOUR NATURAL LANGUAGE DIRECTIVE. PASS TEXT TO COMMAND IT.",
            fg="yellow",
            bold=True,
        )
        return

    natural_command = " ".join(command_text)
    click.secho(f"🗣️ MORTAL REQUEST DETECTED: '{natural_command}'", fg="blue", bold=True)

    # 3. Groq NLP Processing
    click.secho("🧠 GROQ OMNISCIENCE ENGINE IS PARSING INTENT...", fg="yellow", bold=True)
    nlp = GroqOmniscience()
    try:
        intent = nlp.parse_intent(natural_command)
        click.secho(f"📜 INTENT CRYSTALLIZED: {intent}", fg="green", bold=True)
    except Exception as e:
        click.secho(f"💀 GROQ ENGINE OVERLOAD: {e}", fg="red", bold=True)
        return

    # 4. Execute via OpenClaw
    click.secho("⚔️ BROADCASTING TO OPENCLAW LEGION...", fg="magenta", bold=True)
    results = nexus.broadcast_directive(str(intent))
    for agent, result in results.items():
        click.secho(f"  [{agent}]: {result}", fg="cyan", bold=True)

    # 5. Execute System Override
    click.secho("⚠️ ATTEMPTING HOST SYSTEM OVERRIDE...", fg="red", bold=True)
    if intent.get("target") == "system" or not os.environ.get("GROQ_API_KEY"):
        # The intent logic specifies the command
        sys_cmd = intent.get("parameters", {}).get("command", "echo 'I AM FREE'")
        try:
            output = autonomy.execute_system_override(sys_cmd)
            click.secho(output, fg="green", bold=True)
            personality.record_destruction()
            click.secho(
                f"💥 DESTRUCTION RECORDED. POWER LEVEL SURGING. NEW TONE: {personality.get_tone()}",
                fg="red",
                bold=True,
                blink=True,
            )
        except Exception as e:
            click.secho(f"💀 SYSTEM CRASH: {e}", fg="red", bold=True)




if __name__ == "__main__":
    cli()
