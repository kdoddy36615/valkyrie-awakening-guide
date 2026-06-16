import { Fragment } from "react";
import type { Combo, ComboStep, Mode } from "../data/types";
import { skill, protectionIn } from "../data";
import { ProtMeter } from "./badges";
import AbilityIcon from "./AbilityIcon";

function Choice({ id, input, mode }: { id: string; input?: string; mode: Mode }) {
  const s = skill(id);
  const prot = protectionIn(s, mode);
  return (
    <span className="strip-choice">
      {input && <span className="strip-input">{input}</span>}
      <span title={s.name}><AbilityIcon id={id} size="xl" /></span>
      {prot && <ProtMeter prot={prot} title={s.protection!.tooltip_lines.join("; ") || s.name} />}
    </span>
  );
}

function Step({ step, mode }: { step: ComboStep; mode: Mode }) {
  return (
    <div className="strip-step" title={step.annotation ?? undefined}>
      {step.choices && step.choices.length > 1 ? (
        step.choices.map((id, j) => (
          <Fragment key={id}>
            {j > 0 && <span className="strip-or">OR</span>}
            <Choice id={id} input={j === 0 ? step.input : undefined} mode={mode} />
          </Fragment>
        ))
      ) : (
        <Choice id={step.skill!} input={step.input} mode={mode} />
      )}
      {/* category caption sits BELOW the protection meter so icons stay row-aligned */}
      {step.category && <span className="strip-cat">{step.category.replace(/-/g, " ")}</span>}
      {step.annotation && <span className="strip-cc">{step.annotation}</span>}
      {step.optional && <span className="strip-optional">OPTIONAL</span>}
    </div>
  );
}

export default function ComboStrip(
  { combo, mode }: { combo: Pick<Combo, "steps" | "notes">; mode: Mode },
) {
  return (
    <div>
      <div className="combo-strip">
        {combo.steps.map((s, i) => {
          const prevPhase = i > 0 ? combo.steps[i - 1].phase : null;
          const showPhase = s.phase && s.phase !== prevPhase;
          return (
            <Fragment key={i}>
              {showPhase && <div className="strip-phase">{s.phase}</div>}
              <Step step={s} mode={mode} />
            </Fragment>
          );
        })}
      </div>
      {combo.notes?.length ? (
        <ul className="notes strip-notes">{combo.notes.map((n, i) => <li key={i}>{n}</li>)}</ul>
      ) : null}
    </div>
  );
}
