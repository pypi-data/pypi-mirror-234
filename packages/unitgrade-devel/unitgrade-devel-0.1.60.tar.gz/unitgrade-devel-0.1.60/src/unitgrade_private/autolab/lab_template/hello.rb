require "AssessmentBase.rb"

module {{base_name|capitalize}}
  include AssessmentBase

  def assessmentInitialize(course)
    super("{{base_name}}",course)
    @problems = []
  end

end
