exports.verify = (data) => {

  if (!data || !data.fields) {
    return {
      overall_status: "MISSING",
      reason: "No extracted fields found"
    };
  }

  const results = {};

  for (const [name, field] of Object.entries(data.fields)) {
    if (!field.value) {
      results[name] = {
        ...field,
        status: "MISSING"
      };
    }
    else if (field.confidence >= 0.85) {
      results[name] = {
        ...field,
        status: "VERIFIED"
      };
    }
    else if (field.confidence >= 0.60) {
      results[name] = {
        ...field,
        status: "FLAGGED"
      };
    }
    else {
      results[name] = {
        ...field,
        status: "FLAGGED"
      };
    }
  }
  return {
    overall_status: "VERIFIED",
    fields: results
  };
};